from ctypes import *

libc = CDLL("codec/lib/libCodec_lzw.so")

libc.code.argtypes = [POINTER(c_uint8), c_uint32, POINTER(POINTER(c_uint32)), POINTER(c_uint32), c_uint32]
libc.code.restype = c_bool
libc.free_code.argtypes = [POINTER(POINTER(c_uint32))]
libc.free_code.restype = c_void_p
libc.decode.argtypes = [POINTER(c_uint32), c_uint32, POINTER(POINTER(c_uint8)), POINTER(c_uint32)]
libc.decode.restype = c_bool
libc.free_decode.argtypes = [POINTER(POINTER(c_uint8))]
libc.free_decode.restype = c_void_p

c_max_dict_bit_size = 13  # Value has to be between 9 and 32, no more or less


def code(input: bytes):
    c_in_buf = (c_uint8 * len(input)).from_buffer(bytearray(input))
    c_out_buf_len = (c_uint32 * 1)()
    c_out_buf = (POINTER(c_uint32) * 1)()
    ret = libc.code(c_in_buf, c_uint32(len(input)), c_out_buf, c_out_buf_len, c_max_dict_bit_size)
    if ret:
        retVal = [c_out_buf[0][i] for i in range(c_out_buf_len[0])]
        libc.free_code(c_out_buf)
        return retVal


def decode(input: list):
    c_in_buf = (c_uint32 * len(input))(*input)
    c_out_buf_len = (c_uint32 * 1)()
    c_out_buf = (POINTER(c_uint8) * 1)()
    ret = libc.decode(c_in_buf, c_uint32(len(input)), c_out_buf, c_out_buf_len)
    if ret:
        retVal = string_at(c_out_buf[0], c_out_buf_len[0])
        libc.free_decode(c_out_buf)
        return retVal
