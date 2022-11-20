//
// LZW Codec
// WUT project for Data Compression
// Created on 16.11.2022.
//

#ifndef KODA_LZW_CODEC_H
#define KODA_LZW_CODEC_H

#include <map>
#include <vector>
#include <string>
#include <cstdint>
#include <fstream>
#include <iostream>

namespace LZW {

    class Codec {
    public:
        void Coder(std::string& filePath, int dictBitSize);

    private:
        std::vector<uint8_t> ReadFile(std::string filePath, bool verbose = false);
        void WriteFile(std::string fileName);
    };

} // LZW

#endif //KODA_LZW_CODEC_H
