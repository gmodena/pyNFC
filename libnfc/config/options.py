from ctypes import c_int

# config options
DCO_HANDLE_CRC              = c_int(0x00)
DCO_HANDLE_PARITY           = c_int(0x01)
DCO_ACTIVATE_FIELD          = c_int(0x10)
DCO_ACTIVATE_CRYPTO1        = c_int(0x11)
DCO_INFINITE_SELECT         = c_int(0x20)
DCO_ACCEPT_INVALID_FRAMES   = c_int(0x30)
DCO_ACCEPT_MULTIPLE_FRAMES  = c_int(0x31)