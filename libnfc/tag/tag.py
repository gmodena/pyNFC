from ctypes import Structure, Union
from ctypes import c_uint32, c_int, c_char
from libnfc.config import options
from libnfc.types import *

from ctypes import *
# init modulation
IM_ISO14443A_106  = 0
IM_FELICA_212     = 1
IM_FELICA_424     = 2
IM_ISO14443B_106  = 3
IM_JEWEL_106      = 4

class pyTAG_INFO_iso14443a(Structure):
	_pack_ = 1
	_fields_ = [("abtAtqa",  BYTE_T * 2), ("btSak", BYTE_T), ("uiUidLen", c_uint32), ("abtUid", BYTE_T * 10), ("uiAtsLen", c_uint32), ("abtAts", BYTE_T * 36) ]
	def get_abtUid(self):
		uid = []
		for i in self.abtUid:
			uid.append( i.byte_t)

		return uid

	def get_abtAtqa(self):
		uid = []
		for i in self.abtAtqa:
			uid.append(i.byte_t)
		return uid

class pyTAG_INFO_FELICA(Structure):
	_pack_ = 1
	_fields_ = [("uiLen", c_uint32), ("btResCode", BYTE_T), ("abtId", BYTE_T *
        8), ("abtPad", BYTE_T * 8), ("abtSysCode", BYTE_T * 8)]

class pyTAG_INFO_JEWEL(Structure):
	_pack_ = 1
	_fields_ = [("btSensRes", BYTE_T * 2 ), ("btId", BYTE_T * 2)]

class pyTAG_INFO_iso14443b(Structure):
	_pack_ = 1
	_fields_ = [("abtAtqb", BYTE_T * 12), ("abtId", BYTE_T * 4), ("btParam1", BYTE_T), ("btParam2", BYTE_T), ("btParam3", BYTE_T), ("btParam4", BYTE_T), ("btCid", BYTE_T), ("uiInfLen", c_uint32), ("abtInf", BYTE_T * 64) ]



class pyTAG_INFO(Union):
	_pack_ = 1

	_fields_ = [("tia", pyTAG_INFO_iso14443a), ("tif", pyTAG_INFO_FELICA),
                    ("tib", pyTAG_INFO_iso14443b), ("tij", pyTAG_INFO_JEWEL) ]
