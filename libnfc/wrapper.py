from ctypes import CDLL, POINTER
from libnfc import *

class NFCError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        
class Wrapper(object):
    '''
        Wrap functions defined in libnfc/libnfc.h
        Supports all the functions provided by the library version 1.2.1.
    '''
    def __init__(self):     
        try:
            self._libnfc = CDLL('libnfc.so')
        except OSError:
            print "libnfc not found"
        
        self.pdi = None
        self.tag = None
    
        
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
        
        self.pdi = self.libnfc.nfc_connect()[0]
        
        if self.pdi == INVALID_DEVICE_INFO:
            raise NFCError('Invalid device')
        
        
    def disconnect(self):
        '''
            Wraps:
                nfc_disconnect()
        '''
        self._libnfc.nfc_disconnect.restype = c_bool
        self._libnfc.nfc_disconnect.argtypes = [POINTER(pyDEV_INFO)]

        if not self._libnfc.nfc_disconnect(self.pdi):
            raise NFCError('Error while disconnecting the device')
    
      
    def configure(self, config_option, enable):
        self._libnfc.nfc_configure.restype = c_bool
        self._libnfc.nfc_configure.argtypes = [POINTER(pyDEV_INFO), c_int, c_bool]

        if not self.libnfc.nfc_configure(self.pdi, config_option, enable):
            raise NFCError('Error while trying to configure the device')
        
        
    def initiator_init(self):
        '''
            Wraps:
                nfc_initiator_init()
        '''
        self._libnfc.nfc_initiator_init.restype = c_bool
        self._libnfc.nfc_initiator_init.argtypes = [POINTER(pyDEV_INFO)]
        
        if not self._libnfc.nfc_initiator_init(self.pdi):
            raise NFCError('Error while trying to initiate the device')
    
        
    def initiator_select_tag(self, init_modulation, pb_init_data, init_data_len):
        '''
            Wraps:
                nfc_initiator_select_tag()
                
            Tag related information are stored in a pyTAG_INFO object.
            Information related to the selected tag can be accessed via self.tag
            
            
            TODO: provide properties to easilly dispaly information contained in self.tag
        '''
        self.tag = pyTAG_INFO()
        
        self._libnfc.nfc_initiator_select_tag.restype = c_bool
        self._libnfc.nfc_initiator_select_tag.argtypes = [POINTER(pyDEV_INFO), c_int, POINTER(BYTE_T), c_int, POINTER(pyTAG_INFO) ]	
        
        if not self._libnfc.nfc_initiator_select_tag(self.pdi, init_modulation, pb_init_data, init_data_len, self.tag):
            raise NFCError('Error while selecting tag')

    def initiator_deselect_tag(self):
        '''
            Wraps:
                nfc_initiator_deselect_tag()
        '''
        self._libnfc.nfc_initiator_deselect_tag.restype = c_bool
        self._libnfc.nfc_initiator_deselect_tag.argtypes = POINTER(pyDEV_INFO)

        if  self._libnfc.nfc_initiator_deselect_tag(self.pdi):
            self.tag = None
        else:
            raise NFCError('Error while deselecting tag')
    

    def initiator_transceive_bits(self, pbtTx, uiTxBits, pbtTxPar, pbtRx, puiRxBits, pbtRxPar):
        '''
            Wraps:
                bool nfc_initiator_transceive_bits(const dev_info* pdi, const byte_t* pbtTx, 
                                                    const uint32_t uiTxBits, const byte_t* pbtTxPar, 
                                                        byte_t* pbtRx, uint32_t* puiRxBits, byte_t* pbtRxPar);
        '''
        self._libnfc.nfc_initiator_transceive_bits.restype = c_bool
        self._libnfc.nfc_initiator_transceive_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int, POINTER(BYTE_T), POINTER(BYTE_T), POINTER(c_int), POINTER(BYTE_T)]
        
        if not self._libnfc.nfc_initiator_transceive_bits(self.pdi, pbtTx, uiTxBits, pbtTxPar, pbtRx, puiRxBits, pbtRxPar):
            raise NFCError('initiator_transceive_bits failed')
    

    def initiator_transceive_bytes(self, pbtTX, uiTxLen, pbtRx, puiRxLen):
        '''
            Wraps:
                bool nfc_initiator_transceive_bytes(const dev_info* pdi, const byte_t* pbtTx,
                                                    const uint32_t uiTxLen, byte_t* pbtRx,
                                                        uint32_t* puiRxLen);
        '''
        self._libnfc.nfc_initiator_transceive_bytes.restype = c_bool
        self._libnfc.nfc_initiator_transceive_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int, POINTER(BYTE_T),POINTER(c_int)]

        if not self._libnfc.nfc_initiator_transceive_bytes(self.pdi, pbtTX, uiTxLen, pbtRx, puiRxLen):
            raise NFCError('initiator_transceive_bytes failed')
    

    def initiator_mifare_cmd(self, mifare_cmd, ui8Block, mifare_param):
        '''
            Wraps:
                bool nfc_initiator_mifare_cmd(const dev_info* pdi, const mifare_cmd mc, 
                                                    const uint8_t ui8Block, mifare_param* pmp);
        '''
        self._libnfc.nfc_initiator_mifare_cmd.restype = c_bool
        self._libnfc.nfc_initiator_mifare_cmd.argtypes = [POINTER(pyDEV_INFO), c_int, c_uint8, POINTER(pyMIFARE_PARAM) ]
        
        if not self._libnfc.nfc_initiator_mifare_cmd(self.pdi, mifare_cmd, ui8Block, mifare_param):
            raise NFCError('initiator_mifare_cmd failed')
    
        
    def target_init(self, pbtRx, puiRxBits):
        '''
            Wraps:
                bool nfc_target_init(const dev_info* pdi, 
                    byte_t* pbtRx, uint32_t* puiRxBits);
        '''
        self._libnfc.nfc_target_init.restype = c_bool
        self._libnfc.nfc_target_init.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), POINTER(c_uint)]
        
        if not self._libnfc.nfc_target_init(self.pdi, pbtRx, puiRxBits):
            raise NFCError('target_init failed')
    

    def target_receive_bits(self, pbtRX, puiRxBits, pbtRxPar):
        '''
            Wraps:
                bool nfc_target_receive_bits(const dev_info* pdi, byte_t* 
                                                pbtRx, uint32_t* puiRxBits, byte_t* pbtRxPar);
        '''
        self._libnfc.nfc_target_receive_bits.restype = c_bool
        self._libnfc.nfc_target_receive_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), POINTER(c_uint), POINTER(BYTE_T)]
        
        if not self._libnfc.nfc_target_receive_bits(self.pdi, pbtRX, puiRxBits, pbtRxPar):
            raise NFCError('Read error')
    

    def target_receive_bytes(self, pbtRx, puiRxLen):
        '''
            Wraps:
                bool nfc_target_receive_bytes(const dev_info* pdi, byte_t* pbtRx, uint32_t* puiRxLen);
        '''
        self._libnfc.nfc_target_receive_bytes.restype = c_bool
        self._libnfc.nfc_target_receive_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), POINTER(c_uint)]
        
        if not self._libnfc.nfc_target_receive_bytes(self.pdi, pbtRx, puiRxLen):
            raise NFCError('Read error')

    def target_send_bits(self, pbtTX, uiTxBits, pbtTxPar):
        '''
            Wraps:
                bool nfc_target_send_bits(const dev_info* pdi, const byte_t* pbtTx, 
                                            const uint32_t uiTxBits, const byte_t* pbtTxPar);
        '''
        self._libnfc.nfc_target_send_bits.restype = c_bool
        self._libnfc.nfc_target_send_bits.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int, POINTER(BYTE_T) ]
        
        if not self.libnfx.nfc_target_send_bits(self.pdi, pbtTX, uiTxBits, pbtTxPar):
            raise NFCError('Write error')
    
            
    def target_send_bytes(self, pbtTx, uiTxLen):

        '''
            Wraps:
                bool nfc_target_send_bytes(const dev_info* pdi, 
                    const byte_t* pbtTx, const uint32_t uiTxLen);
        '''
        self._libnfc.nfc_target_send_bytes.restype = c_bool
        self._libnfc.nfc_target_send_bytes.argtypes = [POINTER(pyDEV_INFO), POINTER(BYTE_T), c_int]
        
        if not self._libnfc.nfc_target_send_bytes(self.pdi, pbtTx, uiTxLen):
            raise NFCError('Write error')
    
    


