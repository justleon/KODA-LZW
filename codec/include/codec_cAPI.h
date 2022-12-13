//
// LZW Codec API
// WUT project for Data Compression
// Wrapper: Alicja Turowska
//

#ifndef CODEC_CAPI_H
#define CODEC_CAPI_H

#ifdef __cplusplus
  #define EXPORT_C extern "C"
#else
  #define EXPORT_C
#endif

#include <cstdint>
#include <iostream>
#include <map>
#include <vector>
#include <valarray>

EXPORT_C bool code(uint8_t *in_buf, uint32_t in_buf_len,
                   uint32_t **out_buf, uint32_t *out_buf_len, uint32_t dictBitMaxSize);
EXPORT_C void free_code(uint32_t** out_buf);
EXPORT_C bool decode(uint32_t *in_buf, uint32_t in_buf_len, uint8_t **out_buf, uint32_t *out_buf_len);
EXPORT_C void free_decode(uint8_t** out_buf);

#endif // CODEC_CAPI_H