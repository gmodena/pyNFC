"""
Copyright 2010  Gabriele Modena <gm@nowave.it>. All rights reserved.

 Redistribution and use in source and binary forms, with or without modification, are
 permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice, this list of
     conditions and the following disclaimer.

  2. Redistributions in binary form must reproduce the above copyright notice, this list
     of conditions and the following disclaimer in the documentation and/or other materials
     provided with the distribution.

THIS SOFTWARE IS PROVIDED BY Gabriele Modena ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of Gabriele Modena.
"""



from libnfc.wrapper import NFCWrapper
from libnfc.config.options import *
from libnfc.mifare import *
from libnfc.tag import *

if __name__ == '__main__':
	nfc = NFCWrapper()

        nfc.connect() # connect to a device

        # device information are stored in the NFCWrapper().pdi attribute
	print "Connected to NFC reader: ", nfc.pdi.acName

        # device initialization
	nfc.initiator_init()

        # device configuration
	nfc.configure(DCO_ACTIVATE_FIELD, False)
	nfc.configure(DCO_INFINITE_SELECT,False);

	nfc.configure(DCO_HANDLE_CRC,True);
 	nfc.configure(DCO_HANDLE_PARITY,True);

	nfc.configure(DCO_ACTIVATE_FIELD,True);

        # select a MIFARE tag (IM_ISO14443A_106). Tag information are store in the
        # NFCWrapper().tag attribute.
        # See libfc.tag for a list of supported tags.
        try:
	        nfc.initiator_select_tag(IM_ISO14443A_106, None, 0)

                print "ATQA (SENS_RES): ", ' '.join([i for i in map(hex, nfc.tag.tia.abtAtqa)])
                print "UID  (NFCID1): ", ' '.join([i for i in map(hex, nfc.tag.tia.abtUid)[:nfc.tag.tia.uiUidLen]])
                print "SAK  (SEL_RES)", hex(nfc.tag.tia.btSak)

        except: print "No IM_ISO14443A_106 tag found"

        # deselect the MIFARE tag
        nfc.initiator_deselect_tag()

        # disconnect the device
	nfc.disconnect()
