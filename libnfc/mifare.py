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
from ctypes import c_uint8

# MIFARE classic: mifare_cmd
MC_AUTH_A         = c_uint8(0x60)
MC_AUTH_B         = c_uint8(0x61)
MC_READ           = c_uint8(0x30)
MC_WRITE          = c_uint8(0xA0)
MC_TRANSFER       = c_uint8(0xB0)
MC_DECREMENT      = c_uint8(0xC0)
MC_INCREMENT      = c_uint8(0xC1)
MC_STORE          = c_uint8(0xC2)

class pyMIFARE_PARAM_AUTH(Structure):
    _pack_  = 1 
    _fields_ = [("abtKey", c_uint8 * 6), 
                ("abtUid", c_uint8 * 4)]

    def __repr__(self):
        rep = ['%s=%r' % (k, getattr(self, k)) for k in self.__dict__]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(rep))

class pyMIFARE_PARAM_DATA(Structure):
    _pack_ = 1
    _fields_ = [("abtData", c_uint8 * 16)]
    
    def __repr__(self):
        rep = ['%s=%r' % (k, getattr(self, k)) for k in self.__dict__]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(rep))

class pyMIFARE_PARAM_VALUE(Structure):
    _pack_ = 1
    _fields_ = [("abtValue", c_uint8 * 4)]

    def __repr__(self):
        rep = ['%s=%r' % (k, getattr(self, k)) for k in self.__dict__]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(rep))

class pyMIFARE_PARAM(Union):
    _pack_ = 1
    _fields_ = [("mpa", pyMIFARE_PARAM_AUTH), 
                ("mpd", pyMIFARE_PARAM_DATA),
                ("mpv", pyMIFARE_PARAM_VALUE)]

    def __repr__(self):
        rep = ['%s=%r' % (k, getattr(self, k)) for k in self.__dict__]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(rep))
