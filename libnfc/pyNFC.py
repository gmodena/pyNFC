from ctypes import CDLL, POINTER
from libnfc import *

class pyNFCBasic(object):
    def __init__(self):
        self._libnfc = CDLL('libnfc.so')
        self.pdi = None

    def connect(self):
        self._libnfc.nfc_connect.restype = POINTER(pyDEV_INFO)
        self._libnfc.nfc_connect.argtypes = []
        self.pdi = self._libnfc.nfc_connect()[0]

    def disconnect(self):
        self._libnfc.nfc_disconnect.restype = c_bool
        self._libnfc.nfc_disconnect.argtypes = [POINTER(pyDEV_INFO)]
    
        return self._libnfc.nfc_disconnect(self.pdi)
      
    def configure(self, config_option, enable):
        self._libnfc.nfc_configure.restype = c_bool
        self._libnfc.nfc_configure.argtypes = [POINTER(pyDEV_INFO), c_int, c_bool]
    
        return self._libnfc.nfc_configure(self.pdi, config_option, enable)

    def initiator_init(self):
        self._libnfc.nfc_initiator_init.restype = c_bool
        self._libnfc.nfc_initiator_init.argtypes = [POINTER(pyDEV_INFO)]
        
        return self._libnfc.nfc_initiator_init(self.pdi)
        

    def initiator_select_tag(self, init_modulation, pb_init_data, init_data_len):
        self._libnfc.nfc_initiator_select_tag.restype = c_bool
        self._libnfc.nfc_initiator_select_tag.argtypes = [POINTER(pyDEV_INFO), c_int, POINTER(BYTE_T), c_int, POINTER(pyTAG_INFO) ]	
        self.tag = pyTAG_INFO()
    
        return self._libnfc.nfc_initiator_select_tag(self.pdi, init_modulation, pb_init_data, init_data_len, self.tag)

    def initiator_deselect_tag(self):
        self._libnfc.nfc_initiator_deselect_tag.restype = c_bool
        self._libnfc.nfc_initiator_deselect_tag.argtypes = POINTER(pyDEV_INFO)

        return self._libnfc.nfc_initiator_deselect_tag(self.pdi)

    def initiator_transceive_bits(self, pbtTx, uiTxBits, pbtTxPar, pbtRx, puiRxBits, pbtRxPar):
        '''
        bool nfc_initiator_transceive_bits(const dev_info* pdi, const byte_t* pbtTx, const uint32_t uiTxBits, const byte_t* pbtTxPar, byte_t* pbtRx, uint32_t* puiRxBits, byte_t* pbtRxPar);
        '''
        self._libnfc.nfc_initiator_transceive_bits.restype = c_bool
        self._libnfc.nfc_initiator_transceive_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int, POINTER(BYTE_T), POINTER(BYTE_T), POINTER(c_int), POINTER(BYTE_T)]
        
        return self._libnfc.nfc_initiator_transceive_bits(self.pdi, pbtTx, uiTxBits, pbtTxPar, pbtRx, puiRxBits, pbtRxPar)

    def initiator_transceive_bytes(self, pbtTX, uiTxLen, pbtRx, puiRxLen):
        '''
        bool nfc_initiator_transceive_bytes(const dev_info* pdi, const byte_t* pbtTx, const uint32_t uiTxLen, byte_t* pbtRx, uint32_t* puiRxLen);
        '''
        self._libnfc.nfc_initiator_transceive_bytes.restype = c_bool
        self._libnfc.nfc_initiator_transceive_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int, POINTER(BYTE_T),POINTER(c_int)]

        return self._libnfc.nfc_initiator_transceive_bytes(self.pdi, pbtTX, uiTxLen, pbtRx, puiRxLen)

    def initiator_mifare_cmd(self, mifare_cmd, ui8Block, mifare_param):
        '''
        bool nfc_initiator_mifare_cmd(const dev_info* pdi, const mifare_cmd mc, const uint8_t ui8Block, mifare_param* pmp);
        '''
        self._libnfc.nfc_initiator_mifare_cmd.restype = c_bool
        self._libnfc.nfc_initiator_mifare_cmd.argtypes = [POINTER(pyDEV_INFO), c_int, c_uint8, POINTER(pyMIFARE_PARAM) ]
        
        return self._libnfc.nfc_initiator_mifare_cmd(self.pdi, mifare_cmd, ui8Block, mifare_param)
        
    def target_init(self, pbtRx, puiRxBits):
        '''
        bool nfc_target_init(const dev_info* pdi, byte_t* pbtRx, uint32_t* puiRxBits);
        '''
        self._libnfc.nfc_target_init.restype = c_bool
        self._libnfc.nfc_target_init.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), POINTER(c_uint)]
        
        return self._libnfc.nfc_target_init(self.pdi, pbtRx, puiRxBits)	

    def target_receive_bits(self, pbtRX, puiRxBits, pbtRxPar):
        '''
        bool nfc_target_receive_bits(const dev_info* pdi, byte_t* pbtRx, uint32_t* puiRxBits, byte_t* pbtRxPar);
        '''
        self._libnfc.nfc_target_receive_bits.restype = c_bool
        self._libnfc.nfc_target_receive_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), POINTER(c_uint), POINTER(BYTE_T)]
        
        return self._libnfc.nfc_target_receive_bits(self.pdi, pbtRX, puiRxBits, pbtRxPar)

    def target_receive_bytes(self, pbtRx, puiRxLen):
        '''
        bool nfc_target_receive_bytes(const dev_info* pdi, byte_t* pbtRx, uint32_t* puiRxLen);
        '''
        self._libnfc.nfc_target_receive_bytes.restype = c_bool
        self._libnfc.nfc_target_receive_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), POINTER(c_uint)]
        
        return self._libnfc.nfc_target_receive_bytes(self.pdi, pbtRx, puiRxLen)

    def target_send_bits(self, pbtTX, uiTxBits, pbtTxPar):
        '''
        bool nfc_target_send_bits(const dev_info* pdi, const byte_t* pbtTx, const uint32_t uiTxBits, const byte_t* pbtTxPar);
        '''
        self._libnfc.nfc_target_send_bits.restype = c_bool
        self._libnfc.nfc_target_send_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int, POINTER(BYTE_T) ]
        
        return self.libnfx.nfc_target_send_bits(self.pdi, pbtTX, uiTxBits, pbtTxPar)

    def target_send_bytes(self, pbtTx, uiTxLen):
        '''
        bool nfc_target_send_bytes(const dev_info* pdi, const byte_t* pbtTx, const uint32_t uiTxLen);
        '''
        self._libnfc.nfc_target_send_bytes.restype = c_bool
        self._libnfc.nfc_target_send_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int]
        
        return self._libnfc.nfc_target_send_bytes(self.pdi, pbtTx, uiTxLen)
        
class pyNFC(pyNFCBasic):
    pass