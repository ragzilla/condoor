#!/usr/bin/env python2
# =============================================================================
#
# Copyright (c) 2018, Cisco Systems
# All rights reserved.
#
# # Author: Klaudiusz Staniek
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
# =============================================================================
try:
    import click
except ImportError:
    print("Install click python package\n pip install click")
    exit()

import condoor
import urlparse
import errno
import os
import re


class URL(click.ParamType):
    """This is URL type validator."""

    name = 'url'

    def convert(self, value, param, ctx):
        """Convert to URL scheme."""
        if not isinstance(value, tuple):
            parsed = urlparse.urlparse(value)
            if parsed.scheme not in ('telnet', 'ssh'):
                self.fail('invalid URL scheme (%s).  Only telnet and ssh URLs are '
                          'allowed' % parsed, param, ctx)
        return value


def echo_info(conn):
    """Print detected information."""
    click.echo("General information:")
    click.echo(" Hostname: {}".format(conn.hostname))
    click.echo(" HW Family: {}".format(conn.family))
    click.echo(" HW Platform: {}".format(conn.platform))
    click.echo(" SW Type: {}".format(conn.os_type))
    click.echo(" SW Version: {}".format(conn.os_version))
    click.echo(" Prompt: {}".format(conn.prompt))
    click.echo(" Console connection: {}".format(conn.is_console))

    click.echo("\nUDI:")
    click.echo(" PID: {}".format(conn.pid))
    click.echo(" Description: {}".format(conn.description))
    click.echo(" Name: {}".format(conn.name))
    click.echo(" SN: {}".format(conn.sn))
    click.echo(" VID: {}".format(conn.vid))


def normalize_filename(name):
    filename = re.sub(r"\W+", '_', name)
    if not filename.endswith(".txt"):
        filename += ".txt"
    return filename


@click.command()
@click.option("--url", multiple=True, required=True, envvar='CONDOOR_URLS', type=URL(),
              help='The connection url to the host (i.e. telnet://user:pass@hostname). '
                   'The --url option can be repeated to define multiple jumphost urls. '
                   'If no --url option provided the CONDOOR_URLS environment variable is used.')
def run(url):

    log_dir = "/tmp/dmock"
    cmd = [
        'show version',
        'show version brief',
        'show inventory',
        'show inventory chassis',
        'show users',
        'show install active',
        'show install inactive',
        'show install committed',
    ]

    admin_cmd = [
        'show install active',
        'show install committed',
        'show install inactive',
        'show inventory',
        'show inventory chassis',

    ]

    try:
        os.mkdir(log_dir)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            click.echo("{}: {}".format(exc.strerror, exc.filename))
            exit(exc.errno)

    conn = condoor.Connection("aaa", list(url), log_session=True, log_dir=log_dir)
    conn.msg_callback = click.echo
    try:
        conn.connect(force_discovery=True)
        echo_info(conn)

        for command in cmd:
            try:
                result = ""
                filename = normalize_filename(command)
                result = conn.send(command)
                click.echo("\nCommand: {}".format(command))

            except condoor.CommandSyntaxError:
                click.echo("Command unknown: {}".format(command))
                result = conn._chain.ctrl._session.linesep.join(
                    [conn._chain.ctrl._session.before, conn._chain.ctrl._session.after])

            finally:
                fullpath = os.path.join(log_dir, filename)
                with open(fullpath, "w+") as fd:
                    fd.write(result)
                    click.echo("Filename {} written.".format(filename))

        if conn.os_type == 'eXR':
            conn.send('admin')
            for command in admin_cmd:
                try:
                    result = ""
                    filename = 'admin_' + normalize_filename(command)
                    result = conn.send(command)
                    click.echo("\nCommand: {}".format(command))

                except condoor.CommandSyntaxError:
                    click.echo("Command unknown: {}".format(command))
                    result = conn._chain.ctrl._session.linesep.join(
                        [conn._chain.ctrl._session.before, conn._chain.ctrl._session.after])

                finally:
                    fullpath = os.path.join(log_dir, filename)
                    with open(fullpath, "w+") as fd:
                        fd.write(result)
                        click.echo("Filename {} written.".format(filename))
            conn.send('exit')


    except (condoor.ConnectionError, condoor.ConnectionAuthenticationError, condoor.ConnectionTimeoutError,
            condoor.InvalidHopInfoError, condoor.CommandSyntaxError, condoor.CommandTimeoutError,
            condoor.CommandError, condoor.ConnectionError) as excpt:
        click.echo(excpt)
        raise
    finally:
        conn.disconnect()
    return

if __name__ == '__main__':
    run()  # pylint: disable=no-value-for-parameter
