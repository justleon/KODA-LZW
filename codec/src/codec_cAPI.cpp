//
// LZW Codec API
// WUT project for Data Compression
// Wrapper: Alicja Turowska
// Coder impl.: Łukasz Pokorzyński
// Decoder impl.: Magdalena Paszczuk
//

#include <cstdint>
#include <iostream>
#include <map>
#include <vector>
#include <valarray>
#include "codec_cAPI.h"

bool code(uint8_t *in_buf, uint32_t in_buf_len, uint32_t **out_buf, uint32_t *out_buf_len, uint32_t dictBitMaxSize) {
    if (dictBitMaxSize < 9 || dictBitMaxSize > 32) {
        std::cerr << ("Incorrect dictionary word bit size") << std::endl;
        return false;
    }

    std::cout << "CODE" << std::endl;

    //initialize basic dictionary with 255 characters
    std::map<std::basic_string<uint8_t>, int> table;
    for(int i = 0; i < 256; i++) {
        std::basic_string<uint8_t> record {};
        record += uint8_t(i);
        table[record] = i;
    }

    //initialize data types to code the buffer
    uint32_t maxDictSize = pow(2, dictBitMaxSize);
    if (dictBitMaxSize == 32) {
        maxDictSize -= 1; // uint32_t can have value in range 0 - 4294967295
    }

    std::vector<uint32_t> output;
    std::basic_string<uint8_t> p, c;
    p = in_buf[0];
    int index = 1, recordCount = 256;

    //process every character
    while (index < in_buf_len) {
        c = in_buf[index];
        if(table.find(p + c) != table.end()) {
            p += c;
        }
        else {
            if (recordCount < maxDictSize) {
                table[p + c] = recordCount++;
            }
            output.push_back(table[p]);
            p = c;
        }
        index++;
    }
    //add the last code obtained
    output.push_back(table[p]);

    //copy the results to the output buffer
    *out_buf_len = output.size();
    *out_buf = new uint32_t[*out_buf_len];
    for(int i = 0; i < *out_buf_len; ++i) {
        (*out_buf)[i] = output[i];
    }

    return true;
}

void free_code(uint32_t** out_buf) {
    delete[] (*out_buf);
}

bool decode(uint32_t *in_buf, uint32_t in_buf_len, uint8_t **out_buf, uint32_t *out_buf_len) {
    std::cout << "DECODE" << std::endl;

    // Build the dictionary.
    int dictSize = 256;
    std::map<uint32_t, std::basic_string<uint8_t>> dictionary;
    for (int i = 0; i < 256; i++) {
        dictionary[i] = std::basic_string<uint8_t>(1, i);
    }

    std::basic_string<uint8_t> w(1, in_buf[0]);
    std::basic_string<uint8_t> result = w;
    std::basic_string<uint8_t> entry;
    for (int index = 1; index < in_buf_len; ++index) {
        uint32_t k = in_buf[index];
        if (dictionary.count(k)) {
            entry = dictionary[k];
        }
        else if (k == dictSize) {
            entry = w + w[0];
        }
        else {
            std::cerr << ("Bad compressed k") << std::endl;
            return false;
        }
        result += entry;

        // Add w + entry[0] to the dictionary.
        dictionary[dictSize++] = w + entry[0];

        w = entry;
    }

    *out_buf_len = result.length();
    *out_buf = new uint8_t[*out_buf_len];
    for(int i = 0; i < *out_buf_len; ++i) {
        (*out_buf)[i] = result[i];
    }
    return true;
}

void free_decode(uint8_t** out_buf) {
    delete[] (*out_buf);
}