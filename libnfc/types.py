from ctypes import Structure
from ctypes import POINTER
from ctypes import c_uint8, c_char_p, c_int, c_bool, c_char, c_void_p, c_ubyte

from ctypes import *

class BYTE_T(Structure):
    _pack_ = 1
    _fields_ = [("byte_t", c_ubyte)]
    # TODO: rename to pyBYTE_T
    # TODO: add a method for packing/unpacking the array

class pyDEV_CALLBACKS(Structure):
    pass

class pyDEV_INFO(Structure):
    _pack_ = 1
    _fields_ = [ ("pdc", POINTER(pyDEV_CALLBACKS)), ("acName", c_char * 256),
("ct", c_int8), ("ds", c_void_p),  ("bActive", c_bool), ("bCrc", c_bool),
("bPar", c_bool), ("ui8TxBits", c_uint8) ]


pyDEV_CALLBACKS._pack_ = 1
pyDEV_CALLBACKS._fields_ = [("acDriver", c_char_p), ("connect", CFUNCTYPE(POINTER(pyDEV_INFO), c_uint32)),
                ("transceive", CFUNCTYPE(c_bool, c_ubyte, POINTER(c_ubyte),
                c_uint32, POINTER(c_ubyte), POINTER(c_uint32))),
                                ("disconnect", CFUNCTYPE(None ,
                                POINTER(pyDEV_INFO))) ]

