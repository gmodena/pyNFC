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

from ctypes import Structure, Union
from ctypes import c_uint32, c_char, c_uint8
from libnfc.config import options

# init modulation
IM_ISO14443A_106  = c_uint8(0x0)
IM_FELICA_212     = c_uint8(0x1)
IM_FELICA_424     = c_uint8(0x2)
IM_ISO14443B_106  = c_uint8(0x3)
IM_JEWEL_106      = c_uint8(0x4)

class pyTAG_INFO_iso14443a(Structure):
	_pack_ = 1 # align to byte_t

	_fields_ = [("abtAtqa",  c_uint8 * 2), 
                ("btSak", c_uint8), 
                ("uiUidLen", c_uint32), 
                ("abtUid", c_uint8 * 10), 
                ("uiAtsLen", c_uint32), 
                ("abtAts", c_uint8 * 36) ]

    def __repr__(self):
        rep = ['%s=%r' % (k, getattr(self, k)) for k in self.__dict__]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(rep))

class pyTAG_INFO_FELICA(Structure):
	_pack_ = 1 # align to byte_t

	_fields_ = [("uiLen", c_uint32), 
                        ("btResCode", c_uint8), 
                        ("abtId", c_uint8 * 8), 
                        ("abtPad", c_uint8 * 8), 
                        ("abtSysCode", c_uint8 * 8)]
    def __repr__(self):
        rep = ['%s=%r' % (k, getattr(self, k)) for k in self.__dict__]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(rep))

class pyTAG_INFO_JEWEL(Structure):
	_pack_ = 1 # align to byte_t

	_fields_ = [("btSensRes", c_uint8 * 2 ),
                         ("btId", c_uint8 * 2)]
    
    def __repr__(self):
        rep = ['%s=%r' % (k, getattr(self, k)) for k in self.__dict__]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(rep))

class pyTAG_INFO_iso14443b(Structure):
	_pack_ = 1 # align to byte_t

	_fields_ = [("abtAtqb", c_uint8 * 12), 
                        ("abtId", c_uint8 * 4), 
                        ("btParam1", c_uint8), 
                        ("btParam2", c_uint8), 
                        ("btParam3", c_uint8), 
                        ("btParam4", c_uint8), 
                        ("btCid", c_uint8), 
                        ("uiInfLen", c_uint32), 
                        ("abtInf", c_uint8 * 64) ]
    
    def __repr__(self):
        rep = ['%s=%r' % (k, getattr(self, k)) for k in self.__dict__]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(rep))

class pyTAG_INFO(Union):
	_pack_ = 1 # align to byte_t

	_fields_ = [("tia", pyTAG_INFO_iso14443a), 
                        ("tif", pyTAG_INFO_FELICA),
                        ("tib", pyTAG_INFO_iso14443b), 
                        ("tij", pyTAG_INFO_JEWEL) ]
                        
    def __repr__(self):
        rep = ['%s=%r' % (k, getattr(self, k)) for k in self.__dict__]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(rep))
