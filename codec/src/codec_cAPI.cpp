#include "codec_cAPI.h"
#include <cstdio>

bool code(uint8_t* in_buf, uint32_t in_buf_len, uint32_t** out_buf, uint32_t* out_buf_len) {
    printf("CODE\n");
    *out_buf = new uint32_t[in_buf_len];
    *out_buf_len = in_buf_len;
    for(uint32_t i=0u; i<in_buf_len; ++i) {
        (*out_buf)[i] = i;
    }
    return true;
}

void free_code(uint32_t** out_buf) {
    delete[] (*out_buf);
}

bool decode(uint32_t* in_buf, uint32_t in_buf_len, uint8_t** out_buf, uint32_t* out_buf_len) {
    printf("DECODE\n");
    *out_buf = new uint8_t[in_buf_len];
    *out_buf_len = in_buf_len;
    for(uint32_t i=0u; i<in_buf_len; ++i) {
        (*out_buf)[i] = (uint8_t)i;
    }
    return true;
}

void free_decode(uint8_t** out_buf) {
    delete[] (*out_buf);
}