"""
Copyright 2010  Gabriele Modena <gm@nowave.it>. All rights reserved.

 Redistribution and use in source and binary forms, with or without modification, are
 permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice, this list of
     conditions and the following disclaimer.

  2. Redistributions in binary form must reproduce the above copyright notice, this list
     of conditions and the following disclaimer in the documentation and/or other materials
     provided with the distribution.

THIS SOFTWARE IS PROVIDED BY Gabriele Modena ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of Gabriele Modena.
"""


from ctypes import Structure
from ctypes import POINTER, CFUNCTYPE
from ctypes import c_uint8, c_char_p, c_uint32, c_bool, c_char, c_void_p

# Mapping of the dev_callbacks prototype
# I define it here so it can be referenced by pyDEV_INFO,
# but I set the _fields_ attribute later so to make the
# cross reference between the two structures possible.
class pyDEV_CALLBACKS(Structure):
    _pack_ = 1 # align to byte_t

    def __repr__(self):
        return 'pyDEV_CALLBACKS(acDriver=%s, connect=%s, transceive=%s, disconnect=%s )' % (self.acDriver, self.connect, self.transceive, self.disconnect)

class pyDEV_INFO(Structure):
    _pack_ = 1 # align to byte_t
    _fields_ = [("pdc", POINTER(pyDEV_CALLBACKS)), # operations on the pdi are performed via callbacks
                ("acName", c_char * 256), # name of the device, including chip type
                ("ct", c_uint8), # chip type as defined in libnfc.chip
                ("ds", c_void_p), # pointer to the device connection specifications
                ("bActive", c_bool), # Specific to PN35x. Represents wheter the connection was succesfully established or not
                ("bCrc", c_bool), # Mannaged by libnfc.config.options settings. Tells if CRC is automatically handled on the chip or not
                ("bPar", c_bool), # Managed by libnfc.config.options settings. Tells if the PN35x chip handles parity
                ("ui8TxBits", c_uint8) # The last TX setting.
               ]
    def __repr__(self):
        return 'pyDEV_INFO(pdc=%s, acName=%s, ct=%s, ds=%s, bActive=%s, bCrc=%s, bPar=%s, ui8TxBits=%s)' % (self.pdc, self.acName, self.ct, self.ds, self.bActive, self.bCrc, self.bPar, self.ui8TxBits)

# Wrap callbacks used by the library
pyDEV_CALLBACKS._fields_ = [("acDriver", c_char_p), # driver name and description
                ("connect", CFUNCTYPE(POINTER(pyDEV_INFO), c_uint32)), # callback to *_connect() functions.
                ("transceive", CFUNCTYPE(c_bool, c_uint8, POINTER(c_uint8),
                                c_uint32, POINTER(c_uint8), POINTER(c_uint32))), # callback to *_transceive functions
                ("disconnect", CFUNCTYPE(None, POINTER(pyDEV_INFO))) # callback for *_disconnect functions
                ]
