# =============================================================================
#
# Copyright (c) 2017, Cisco Systems
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

from unittest import TestCase

platform_strings = """Cisco A901-6CZ-FT-A (P2020) processor (revision 1.0) with 393216K/131072K bytes of memory.
cisco ASR-903 (RSP2) processor (revision RSP2) with 918638K/6147K bytes of memory.
cisco ASR-920-12CZ-A (Freescale P2020) processor (revision 1.0 GHz) with 910182K/6147K bytes of memory.
  cisco Nexus9000 C9508 (8 Slot) Chassis ("Supervisor Module")
cisco NCS1002 () processor
cisco NCS-4000 () processor
cisco NCS-5500 () processor
cisco NCS-5002 () processor
cisco NCS-6000 () processor
cisco IOS XRv x64 () processor
cisco IOS-XRv 9000 () processor
cisco ASR9K () processor
cisco ASR9K Series (Intel 686 F6M14S4) processor with 33554432K bytes of memory.
cisco CRS-16/S-B (Intel 686 F6M14S4) processor with 12582912K bytes of memory.
"""


class TestPlatformStringMarching(TestCase):
    def setUp(self):
        pass

    def test_platform_string_match(self):
        pass