"""
Python bindings for libnfc - http://code.google.com/p/libnfc/

Released under the terms of the BSD license. See: 

"""
#!/usr/bin/evn python2.6

from ctypes import *

# chip type
CT_PN531                    = c_int(0x10)
CT_PN532                    = c_int(0x20)
CT_PN533                    = c_int(0x30)

# config options
DCO_HANDLE_CRC              = c_int(0x00)
DCO_HANDLE_PARITY           = c_int(0x01)
DCO_ACTIVATE_FIELD          = c_int(0x10)
DCO_ACTIVATE_CRYPTO1        = c_int(0x11)
DCO_INFINITE_SELECT         = c_int(0x20)
DCO_ACCEPT_INVALID_FRAMES   = c_int(0x30)
DCO_ACCEPT_MULTIPLE_FRAMES  = c_int(0x31)

# init modulation
IM_ISO14443A_106  = c_int(0x00)
IM_FELICA_212     = c_int(0x01)
IM_FELICA_424     = c_int(0x02)
IM_ISO14443B_106  = c_int(0x03)
IM_JEWEL_106      = c_int(0x04)

# MIFARE classic: mifare_cmd
MC_AUTH_A         = c_int(0x60)
MC_AUTH_B         = c_int(0x61)
MC_READ           = c_int(0x30)
MC_WRITE          = c_int(0xA0)
MC_TRANSFER       = c_int(0xB0)
MC_DECREMENT      = c_int(0xC0)
MC_INCREMENT      = c_int(0xC1)
MC_STORE          = c_int(0xC2)

# 

class BYTE_T(Structure):
    _fields_ = [("byte_t", c_uint8)]

class pyDEV_CALLBACKS(Structure):
        _fields_ = [("acDriver", c_char_p) ]

class pyDEV_INFO(Structure):
    _fields_ = [ ("pdc", POINTER(pyDEV_CALLBACKS)), ("chip_type", c_int),
            ("ds", c_int), ("acName", c_char * 256), ("bActive", c_bool), ("bCrc", c_bool), ("bPar", c_bool) ]

class pyTAG_INFO_iso14443a(Structure):
    _fields_ = [("abtAtqa",  BYTE_T * 2), ("btSak", BYTE_T), ("abtUid", BYTE_T *
        10), ("uiAtsLen", c_uint32), ("abtAts", BYTE_T * 36) ]

class pyTAG_INFO_FELICA(Structure):
    _fields_ = [("uiLen", c_uint32), ("btResCode", BYTE_T), ("abtId", BYTE_T *
        8), ("abtPad", BYTE_T * 8), ("abtSysCode", BYTE_T * 8)]

class pyTAG_INFO_JEWEL(Structure):
    _fields_ = [("btSensRes", BYTE_T * 2 ), ("btId", BYTE_T * 2)]

class pyTAG_INFO_iso14443b(Structure):
    _fields_ = [ ("abtAtqb", BYTE_T * 12), ("abtId", BYTE_T * 4), ("btParam1",
        BYTE_T), ("btParam2", BYTE_T), ("btParam3", BYTE_T), ("btParam4",
            BYTE_T), ("btCid", BYTE_T), ("uiInfLen", c_uint32), ("abtInf",
                BYTE_T * 64),  ]

class pyTAG_INFO(Union):
        _fields_ = [("tia", pyTAG_INFO_iso14443a), ("tif", pyTAG_INFO_FELICA),
                    ("tib", pyTAG_INFO_iso14443b), ("tij", pyTAG_INFO_JEWEL) ]

class pyMIFARE_PARAM_AUTH(Structure):
    _fields_ = [("abtKey", BYTE_T * 6), ("abtUid", BYTE_T * 4)]

class pyMIFARE_PARAM_DATA(Structure):
    _fields_ = [("abtData", BYTE_T * 16)]

class pyMIFARE_PARAM_VALUE(Structure):
    _fields_ = [("abtValue", BYTE_T * 4)]

class pyMIFARE_PARAM(Union):
    _fields_ = [("mpa", pyMIFARE_PARAM_AUTH), ("mpd", pyMIFARE_PARAM_DATA),
            ("mpv", pyMIFARE_PARAM_VALUE)]

class pyNFC(object):
  def __init__(self):
    self.libnfc = CDLL('libnfc.so')
    self.pdi = None

  def connect(self):
    self.libnfc.nfc_connect.restype = POINTER(pyDEV_INFO)
    self.libnfc.nfc_connect.argtypes = []
    self.pdi = self.libnfc.nfc_connect()[0]

  def disconnect(self):
    self.libnfc.nfc_disconnect.restype = c_bool
    self.libnfc.nfc_disconnect.argtypes = [POINTER(pyDEV_INFO)]
    
    return self.libnfc.nfc_disconnect(self.pdi)
      
  def configure(self, config_option, enable):
    self.libnfc.nfc_configure.restype = c_bool
    self.libnfc.nfc_configure.argtypes = [POINTER(pyDEV_INFO), c_int, c_bool]
    
    return self.libnfc.nfc_configure(self.pdi, config_option, enable)

  def initiator_init(self):
    self.libnfc.nfc_initiator_init.restype = c_bool
    self.libnfc.nfc_initiator_init.argtypes = [POINTER(pyDEV_INFO)]
    return self.libnfc.nfc_initiator_init(self.pdi)


  def initiator_select_tag(self, init_modulation, pb_init_data, init_data_len):
    self.libnfc.nfc_initiator_select_tag.restype = c_bool
    self.libnfc.nfc_initiator_select_tag.argtypes = [POINTER(pyDEV_INFO), c_int, POINTER(BYTE_T), c_int, POINTER(pyTAG_INFO) ]	
    self.tag = pyTAG_INFO()
    
    return self.libnfc.nfc_initiator_select_tag(self.pdi, init_modulation, pb_init_data, init_data_len, self.tag)

  def initiator_deselect_tag(self):
    self.libnfc.nfc_initiator_deselect_tag.restype = c_bool
    self.libnfc.nfc_initiator_deselect_tag.argtypes = POINTER(pyDEV_INFO)

    return self.libnfc.nfc_initiator_deselect_tag(self.pdi)

  def initiator_transceive_bits(self, pbtTx, uiTxBits, pbtTxPar, pbtRx, puiRxBits, pbtRxPar):
    '''
      bool nfc_initiator_transceive_bits(const dev_info* pdi, const byte_t* pbtTx, const uint32_t uiTxBits, const byte_t* pbtTxPar, byte_t* pbtRx, uint32_t* puiRxBits, byte_t* pbtRxPar);
      '''
    self.libnfc.nfc_initiator_transceive_bits.restype = c_bool
    self.libnfc.nfc_initiator_transceive_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int, POINTER(BYTE_T), POINTER(BYTE_T), POINTER(c_int), POINTER(BYTE_T)]

    return self.libnfc.nfc_initiator_transceive_bits(self.pdi, pbtTx, uiTxBits, pbtTxPar, pbtRx, puiRxBits, pbtRxPar)

  def initiator_transceive_bytes(self, pbtTX, uiTxLen, pbtRx, puiRxLen):
    '''
    bool nfc_initiator_transceive_bytes(const dev_info* pdi, const byte_t* pbtTx, const uint32_t uiTxLen, byte_t* pbtRx, uint32_t* puiRxLen);
    '''
    self.libnfc.nfc_initiator_transceive_bytes.restype = c_bool
    self.libnfc.nfc_initiator_transceive_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int, POINTER(BYTE_T),POINTER(c_int)]
    
    return self.libnfc.nfc_initiator_transceive_bytes(self.pdi, pbtTX, uiTxLen, pbtRx, puiRxLen)

  def initiator_mifare_cmd(self, mifare_cmd, ui8Block, mifare_param):
    '''
    bool nfc_initiator_mifare_cmd(const dev_info* pdi, const mifare_cmd mc, const uint8_t ui8Block, mifare_param* pmp);
    '''
    self.libnfc.nfc_initiator_mifare_cmd.restype = c_bool
    self.libnfc.nfc_initiator_mifare_cmd.argtypes = [POINTER(pyDEV_INFO), c_int, c_uint8, POINTER(pyMIFARE_PARAM) ]
    return self.libnfc.nfc_initiator_mifare_cmd(self.pdi, mifare_cmd, ui8Block, mifare_param)


  def target_init(self, pbtRx, puiRxBits):
    '''
    bool nfc_target_init(const dev_info* pdi, byte_t* pbtRx, uint32_t* puiRxBits);
    '''
    self.libnfc.nfc_target_init.restype = c_bool
    self.libnfc.nfc_target_init.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), POINTER(c_uint)]
    return self.libnfc.nfc_target_init(self.pdi, pbtRx, puiRxBits)	

  def target_receive_bits(self, pbtRX, puiRxBits, pbtRxPar):
    '''
    bool nfc_target_receive_bits(const dev_info* pdi, byte_t* pbtRx, uint32_t* puiRxBits, byte_t* pbtRxPar);
    '''
    self.libnfc.nfc_target_receive_bits.restype = c_bool
    self.libnfc.nfc_target_receive_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), POINTER(c_uint), POINTER(BYTE_T)]
    return self.libnfc.nfc_target_receive_bits(self.pdi, pbtRX, puiRxBits, pbtRxPar)

  def target_receive_bytes(self, pbtRx, puiRxLen):
    '''
    bool nfc_target_receive_bytes(const dev_info* pdi, byte_t* pbtRx, uint32_t* puiRxLen);
    '''
    self.libnfc.nfc_target_receive_bytes.restype = c_bool
    self.libnfc.nfc_target_receive_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), POINTER(c_uint)]
    return self.libnfc.nfc_target_receive_bytes(self.pdi, pbtRx, puiRxLen)

  def target_send_bits(self, pbtTX, uiTxBits, pbtTxPar):
    '''
    bool nfc_target_send_bits(const dev_info* pdi, const byte_t* pbtTx, const uint32_t uiTxBits, const byte_t* pbtTxPar);
    '''
    self.libnfc.nfc_target_send_bits.restype = c_bool
    self.libnfc.nfc_target_send_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int, POINTER(BYTE_T) ]
    return self.libnfx.nfc_target_send_bits(self.pdi, pbtTX, uiTxBits, pbtTxPar)

  def target_send_bytes(self, pbtTx, uiTxLen):
    '''
    bool nfc_target_send_bytes(const dev_info* pdi, const byte_t* pbtTx, const uint32_t uiTxLen);
    '''
    self.libnfc.nfc_target_send_bytes.restype = c_bool
    self.libnfc.nfc_target_send_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int]
    return self.libnfc.nfc_target_send_bytes(self.pdi, pbtTx, uiTxLen)

if __name__ == "__main__":
  nfc = pyNFC()
  nfc.connect()
	print nfc.pdi.acName
	print nfc.pdi.chip_type

	print nfc.initiator_init()

	print nfc.configure(DCO_ACTIVATE_FIELD, False)
	print nfc.configure(DCO_INFINITE_SELECT,False);

  	print nfc.configure(DCO_HANDLE_CRC,True);
	print nfc.configure(DCO_HANDLE_PARITY,True);

  	print nfc.configure(DCO_ACTIVATE_FIELD,True);

	
	nfc.initiator_select_tag(IM_ISO14443A_106, None, 0)

	print nfc.tag.tia.abtUid[0].byte_t

	print nfc.disconnect()
