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




from ctypes import CDLL, POINTER, CFUNCTYPE, byref, c_uint8, c_uint32, c_bool

from libnfc.types import *

from libnfc.config.options import *
from libnfc.chip import *
from libnfc.tag import *
from libnfc.mifare import *

from ctypes import *

import os

class NFCError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
	    pass


class NFCWrapper(object):
    '''
        Wrap functions defined in libnfc/libnfc.h
        Supports all the functions provided by the library version 1.2.1.
    '''
    def __init__(self):
		if os.name ==  "posix":
			try: self._libnfc = CDLL('libnfc.so')
			except OSError: print "libnfc not found"
		else: raise NFCError("pyNCF does not support %s platfom", os.name)

        # Initialize local structures
		self.pdi = None # stores device information, later bound to a pyDEV_INFO pointer
		self.tag = pyTAG_INFO() # stores tag information
		self.mifare_param = pyMIFARE_PARAM() # stores data generated upon querying a mifare card

    def __cfunc(name, dll, result, *args):
        atypes = []
        aflags = []

        for arg in args:
            atypes.append(arg[1])
            aflags.append((arg[2], arg[0]) + arg[3:])

        return CFUNCTYPE(result, *atypes)((name, dll), tuple(aflags))

    def connect(self):
        '''
            Wraps:
                nfc_connect()
            The device information is stored in a class instance of pyDEV_INFO.
            Information related to the device can be accessed via self.pdi
            TODO: provide properties to easilly dispaly information contained in self.pdi
        '''
        self._libnfc.nfc_connect.restype = POINTER(pyDEV_INFO)
        self._libnfc.nfc_connect.argtypes = []
        

        self.pdi = self._libnfc.nfc_connect()[0] 
        
        if self.pdi == INVALID_DEVICE_INFO:
            raise NFCError('Invalid device')
        else: return True
        
    def disconnect(self):
        '''
            Wraps:
                nfc_disconnect()
        '''
        self._libnfc.nfc_disconnect.restype = c_bool
        self._libnfc.nfc_disconnect.argtypes = [POINTER(pyDEV_INFO)]

        if not self._libnfc.nfc_disconnect(byref(self.pdi)):
            raise NFCError('Error while disconnecting the device')
    	else: return True
      
    def configure(self, config_option, enable):
        self._libnfc.nfc_configure.restype = c_bool
        self._libnfc.nfc_configure.argtypes = [POINTER(pyDEV_INFO), c_ubyte, c_bool]

        if not self._libnfc.nfc_configure(byref(self.pdi), config_option, enable):
            raise NFCError('Error while trying to configure the device')
        else: return True
        
    def initiator_init(self):
		'''
            Wraps:
                nfc_initiator_init()
		'''
		self._libnfc.nfc_initiator_init.restype = c_bool
		self._libnfc.nfc_initiator_init.argtypes = [POINTER(pyDEV_INFO)]
        
		if not self._libnfc.nfc_initiator_init(byref(self.pdi)):
			raise NFCError('Error while trying to initiate the device')
		else: return True    
        
    def initiator_select_tag(self, init_modulation, pb_init_data, init_data_len):
		'''
            Wraps:
               bool nfc_initiator_select_tag(const dev_info* pdi, const init_modulation im, const byte_t* pbtInitData, const uint32_t uiInitDataLen, tag_info* pti); 
            Tag related information are stored in a pyTAG_INFO object.
            Information related to the selected tag can be accessed via self.tag
            
            
            TODO: provide properties to easilly dispaly information contained in self.tag
		'''
        if pbInitData: pbInitData = byref(POINTER(c_uint8))

		self._libnfc.nfc_initiator_select_tag.restype = c_bool
		self._libnfc.nfc_initiator_select_tag.argtypes = [POINTER(pyDEV_INFO), c_ubyte, POINTER(c_uint8), c_uint32, POINTER(pyTAG_INFO) ]	
        
		if not self._libnfc.nfc_initiator_select_tag(byref(self.pdi), init_modulation, pb_init_data, init_data_len, byref(self.tag)):
			raise NFCError('Error while selecting tag')
		else: return True

    def initiator_deselect_tag(self):
		'''
            Wraps:
                nfc_initiator_deselect_tag()
		'''
		self._libnfc.nfc_initiator_deselect_tag.restype = c_bool
		self._libnfc.nfc_initiator_deselect_tag.argtypes = [POINTER(pyDEV_INFO)]

		if  self._libnfc.nfc_initiator_deselect_tag(byref(self.pdi)):
			self.tag = None
			return True
		else: raise NFCError('Error while deselecting tag')
    

    def initiator_transceive_bits(self, pbtTx, uiTxBits, pbtTxPar, pbtRx, puiRxBits, pbtRxPar):
        '''
            Wraps:
                bool nfc_initiator_transceive_bits(const dev_info* pdi, const byte_t* pbtTx, 
                                                    const uint32_t uiTxBits, const byte_t* pbtTxPar, 
                                                        byte_t* pbtRx, uint32_t* puiRxBits, byte_t* pbtRxPar);
        '''
        self._libnfc.nfc_initiator_transceive_bits.restype = c_bool
        self._libnfc.nfc_initiator_transceive_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(c_uint8), c_uint32, POINTER(c_uint8), POINTER(c_uint8), POINTER(c_uint32), POINTER(c_uint8)]
        
        if not self._libnfc.nfc_initiator_transceive_bits(byref(self.pdi), pbtTx, uiTxBits, pbtTxPar, pbtRx, uiRxBits, pbtRxPar):
            raise NFCError('initiator_transceive_bits failed')
    	else: return True

    def initiator_transceive_bytes(self, pbtTX, uiTxLen, pbtRx, puiRxLen):
        '''
            Wraps:
                bool nfc_initiator_transceive_bytes(const dev_info* pdi, const byte_t* pbtTx,
                                                    const uint32_t uiTxLen, byte_t* pbtRx,
                                                        uint32_t* puiRxLen);
        '''
        self._libnfc.nfc_initiator_transceive_bytes.restype = c_bool
        self._libnfc.nfc_initiator_transceive_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(c_uint8), c_uint32, POINTER(c_uint8), POINTER(c_uint32)]

        if not self._libnfc.nfc_initiator_transceive_bytes(byref(self.pdi), pbtTX, uiTxLen, pbtRx, puiRxLen):
            raise NFCError('initiator_transceive_bytes failed')
    	else: return True

    def initiator_mifare_cmd(self, mifare_cmd, ui8Block):
		'''
            Wraps:
                bool nfc_initiator_mifare_cmd(const dev_info* pdi, const mifare_cmd mc, 
                                                    const uint8_t ui8Block, mifare_param* pmp);
		'''
		self._libnfc.nfc_initiator_mifare_cmd.restype = c_bool
		self._libnfc.nfc_initiator_mifare_cmd.argtypes = [POINTER(pyDEV_INFO), c_uint8, c_uint8, POINTER(pyMIFARE_PARAM) ]
        
		if not self._libnfc.nfc_initiator_mifare_cmd(byref(self.pdi), mifare_cmd, ui8Block, byref(self.mifare_param)):
			raise NFCError('initiator_mifare_cmd failed')
		else: return True
        
    def target_init(self, pbtRx, puiRxBits):
        '''
            Wraps:
                bool nfc_target_init(const dev_info* pdi, 
                    byte_t* pbtRx, uint32_t* puiRxBits);
        '''
        self._libnfc.nfc_target_init.restype = c_bool
        self._libnfc.nfc_target_init.argtypes = [POINTER(pyDEV_INFO), POINTER(c_uint8), POINTER(c_uint32)]
        
        if not self._libnfc.nfc_target_init(byref(self.pdi), pbtRx, puiRxBits):
            raise NFCError('target_init failed')
    	else: return True

    def target_receive_bits(self, pbtRX, puiRxBits, pbtRxPar):
        '''
            Wraps:
                bool nfc_target_receive_bits(const dev_info* pdi, byte_t* 
                                                pbtRx, uint32_t* puiRxBits, byte_t* pbtRxPar);
        '''
        self._libnfc.nfc_target_receive_bits.restype = c_bool
        self._libnfc.nfc_target_receive_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(c_uint8), POINTER(c_uint32), POINTER(c_uint8)]
        
        if not self._libnfc.nfc_target_receive_bits(byref(self.pdi), pbtRX, puiRxBits, pbtRxPar):
            raise NFCError('Read error')
    	else: return True

    def target_receive_bytes(self, pbtRx, puiRxLen):
		'''
            Wraps:
                bool nfc_target_receive_bytes(const dev_info* pdi, byte_t* pbtRx, uint32_t* puiRxLen);
		'''
		self._libnfc.nfc_target_receive_bytes.restype = c_bool
		self._libnfc.nfc_target_receive_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(c_uint8), POINTER(c_uint32)]
        
		if not self._libnfc.nfc_target_receive_bytes(byref(self.pdi), pbtRx, puiRxLen): raise NFCError('Read error')
		else: return True

    def target_send_bits(self, pbtTX, uiTxBits, pbtTxPar):
        '''
            Wraps:
                bool nfc_target_send_bits(const dev_info* pdi, const byte_t* pbtTx, 
                                            const uint32_t uiTxBits, const byte_t* pbtTxPar);
        '''
        self._libnfc.nfc_target_send_bits.restype = c_bool
        self._libnfc.nfc_target_send_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(c_uint8), c_uint32, POINTER(c_uint8) ]
        
        if not self.libnfx.nfc_target_send_bits(byref(self.pdi), pbtTX, uiTxBits, pbtTxPar):
            raise NFCError('Write error')
    	else: return True
            
    def target_send_bytes(self, pbtTx, uiTxLen):

        '''
            Wraps:
                bool nfc_target_send_bytes(const dev_info* pdi, 
                    const byte_t* pbtTx, const uint32_t uiTxLen);
        '''
        self._libnfc.nfc_target_send_bytes.restype = c_bool
        self._libnfc.nfc_target_send_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(c_uint8), c_uint32]
        
        if not self._libnfc.nfc_target_send_bytes(byref(self.pdi), pbtTx, uiTxLen):
            raise NFCError('Write error')
    	else: return True
 
    def __repr__(self):
        return 'NFCWrapper(pdi=%s, tag=%s, mifare_param=%s)' % (self.pdi, self.tag, self.mifare_param)


