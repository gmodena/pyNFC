from ctypes import Structure, Union
from ctypes import c_int
from libnfc.types import BYTE_T

# MIFARE classic: mifare_cmd
MC_AUTH_A         = c_int(0x60)
MC_AUTH_B         = c_int(0x61)
MC_READ           = c_int(0x30)
MC_WRITE          = c_int(0xA0)
MC_TRANSFER       = c_int(0xB0)
MC_DECREMENT      = c_int(0xC0)
MC_INCREMENT      = c_int(0xC1)
MC_STORE          = c_int(0xC2)

class pyMIFARE_PARAM_AUTH(Structure):
    _fields_ = [("abtKey", BYTE_T * 6), ("abtUid", BYTE_T * 4)]

class pyMIFARE_PARAM_DATA(Structure):
    _fields_ = [("abtData", BYTE_T * 16)]

class pyMIFARE_PARAM_VALUE(Structure):
    _fields_ = [("abtValue", BYTE_T * 4)]

class pyMIFARE_PARAM(Union):
    _fields_ = [("mpa", pyMIFARE_PARAM_AUTH), ("mpd", pyMIFARE_PARAM_DATA),
            ("mpv", pyMIFARE_PARAM_VALUE)]