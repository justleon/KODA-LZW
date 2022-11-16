//
// LZW Codec
// WUT project for Data Compression
// Created on 16.11.2022.
//

#ifndef KODA_LZW_CODEC_H
#define KODA_LZW_CODEC_H

#include <vector>
#include <string>
#include <cstdint>
#include <fstream>
#include <iostream>

namespace LZW {

    class Codec {
    public:
        void coder(std::string filePath);

    private:
        std::vector<uint8_t> read(std::string filePath, bool verbose = false);

    };

} // LZW

#endif //KODA_LZW_CODEC_H
