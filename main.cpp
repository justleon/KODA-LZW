//
// Main codec program
// WUT project for Data Compression
// Created on 16.11.2022.
//

#include "codec_src/Codec.h"

int main(int argc, char **argv) {
    if(argc <= 1 || argc > 2) {
        std::cerr << "Wrong number of arguments" << std::endl;
        return 1;
    }

    LZW::Codec codec;
    std::string filePath = argv[1];
    codec.Coder(filePath, 20);

    return 0;
}