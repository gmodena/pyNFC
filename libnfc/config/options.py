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

from ctypes import c_ubyte, c_int

# config options
DCO_HANDLE_CRC              = c_ubyte(0x00)
DCO_HANDLE_PARITY           = c_ubyte(0x01)
DCO_ACTIVATE_FIELD          = c_ubyte(0x10)
DCO_ACTIVATE_CRYPTO1        = c_ubyte(0x11)
DCO_INFINITE_SELECT         = c_ubyte(0x20)
DCO_ACCEPT_INVALID_FRAMES   = c_ubyte(0x30)
DCO_ACCEPT_MULTIPLE_FRAMES  = c_ubyte(0x31)


# Labels defined in include/defines.h
INVALID_DEVICE_INFO         = c_ubyte(0)
MAX_FRAME_LEN               = c_int(264)
DEVICE_NAME_LENGTH          = c_ubyte(256)
MAX_DEVICES                 = c_ubyte(16)
