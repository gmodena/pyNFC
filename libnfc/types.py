from ctypes import Structure
from ctypes import POINTER
from ctypes import c_uint8, c_char_p, c_int, c_bool, c_char


class BYTE_T(Structure):
    _fields_ = [("byte_t", c_uint8)]

class pyDEV_CALLBACKS(Structure):
        _fields_ = [("acDriver", c_char_p) ]

class pyDEV_INFO(Structure):
    _fields_ = [ ("pdc", POINTER(pyDEV_CALLBACKS)), ("chip_type", c_int),
            ("ds", c_int), ("acName", c_char * 256), ("bActive", c_bool), ("bCrc", c_bool), ("bPar", c_bool) ]
            