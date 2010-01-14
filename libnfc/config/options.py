from ctypes import c_int

# config options
DCO_HANDLE_CRC              = c_int(0x00)
DCO_HANDLE_PARITY           = c_int(0x01)
DCO_ACTIVATE_FIELD          = c_int(0x10)
DCO_ACTIVATE_CRYPTO1        = c_int(0x11)
DCO_INFINITE_SELECT         = c_int(0x20)
DCO_ACCEPT_INVALID_FRAMES   = c_int(0x30)
DCO_ACCEPT_MULTIPLE_FRAMES  = c_int(0x31)


# Labels defined in include/defines.h
INVALID_DEVICE_INFO         = c_int(0)
MAX_FRAME_LEN               = c_int(264)
DEVICE_NAME_LENGTH          = c_int(256)
MAX_DEVICES                 = c_int(16)
