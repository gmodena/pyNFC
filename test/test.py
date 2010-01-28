#!/usr/bin/env python2.6
#Copyright 2010  Gabriele Modena <gm@nowave.it>. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this list of
#     conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice, this list
#     of conditions and the following disclaimer in the documentation and/or other materials
#     provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY Gabriele Modena ``AS IS'' AND ANY EXPRESS OR IMPLIED
#WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
#CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those of the
#authors and should not be interpreted as representing official policies, either expressed
#or implied, of Gabriele Modena.

__author__ = 'gm@nowave.it'
__version__ = '0.1-devel'



import unittest

from libnfc.wrapper import NFCWrapper
from libnfc.config.options import *
from libnfc.mifare import *
from libnfc.tag import *



# Test values are hardcoded and tailored according to my setup.
# Reader: Alcatel-lucent TouchTag
# Tag: Mifare 4k
#
# TODO: include a card dump so to allow proper test replication.
DEVICE_NAME = "ACR122U102 - PN532 v1.4 (0x07)"
CHIP_TYPE = 32
ATQA = "0x0 0x44"
UID = "0x4 0xc9 0x7f 0x8a 0x35 0x1e 0x80"
SAK = "0x0"

class ConnectSelectDisconnectTest(unittest.TestCase):
    def setUp(self):
        self.nfc = NFCWrapper()

    def runTest(self):
        assert self.nfc.connect() == True, 'Connection not established'
        assert self.nfc.pdi.acName == DEVICE_NAME, 'Incorrect device name'
        assert self.nfc.pdi.ct == CHIP_TYPE, 'Incorrect device chip type'
        assert self.nfc.initiator_init() == True, 'Device initialisation  failed'

        assert self.nfc.configure(DCO_ACTIVATE_FIELD, False) == True, 'Incorrect configuration option'
        assert self.nfc.configure(DCO_INFINITE_SELECT,False) == True, 'Incorrect configuration option'
        assert self.nfc.configure(DCO_HANDLE_CRC,True)  == True, 'Incorrect configuration option'
        assert self.nfc.configure(DCO_HANDLE_PARITY,True) == True, 'Incorrect configuration option'
        assert self.nfc.configure(DCO_ACTIVATE_FIELD,True) == True, 'Incorrect configuration option'


        assert self.nfc.initiator_select_tag(IM_ISO14443A_106, None, 0) == None,'Mifare 4k tag selection failed' 

        if self.nfc.tag:
            atqa = ' '.join([i for i in map(hex, self.nfc.tag.tia.abtAtqa)])
            assert atqa == ATQA, 'Incorrect ATQA for Mifare 4k tag'

            uid = ' '.join([i for i in map(hex, self.nfc.tag.tia.abtUid)[:self.nfc.tag.tia.uiUidLen]])
            assert uid  == UID, 'incorrect UID for Mifare 4k tag'

            sak = hex(self.nfc.tag.tia.btSak)
            assert sak == SAK, 'Incorrect SAK for Mifare 4k tag'

            assert self.nfc.initiator_deselect_tag() == True, 'Mifare 4k tag de-selection failed'

        assert self.nfc.disconnect() == True, 'Disconnection failed'


if __name__ == '__main__':
    test1 = ConnectSelectDisconnectTest()
    test1.setUp()
    test1.runTest()
