//
// LZW Codec
// WUT project for Data Compression
// Created on 16.11.2022.
//

#include <map>
#include "Codec.h"

namespace LZW {

    void EmitCode(int code) {
        std::cout << "<" << code << ">";
    }

    void Codec::coder(std::string filePath) {
        std::map<std::string, int> table;
        for(int i = 0; i < 256; i++) {
            std::string record {};
            record += uint8_t(i);
            table[record] = i;
        }

        std::vector<uint8_t> buffer = read(filePath, true);
        std::string p, c;
        p = buffer[0];
        int index = 1;
        int recordCount = 256;
        while (index < buffer.size()) {
            c = buffer[index];
            if(table.find(p + c) != table.end()) {
                p += c;
            }
            else {
                table[p+c] = recordCount++;
                EmitCode(table[p]);
                p = c;
            }
            index++;
        }
        EmitCode(table[p]);
    }

    std::vector<uint8_t> Codec::read(std::string filePath, bool verbose) {
        std::ifstream file(filePath, std::ios::binary);
        if(file) {
            std::streampos begOfFile, endOfFile;
            file.seekg(0, std::ios::end);
            endOfFile = file.tellg();
            file.seekg(0, std::ios::beg);
            begOfFile = file.tellg();

            long fileSize = endOfFile - begOfFile;
            if (fileSize == 0) {
                std::cout << "File is empty." << std::endl;
                return std::vector<uint8_t>{};
            }

            std::vector<uint8_t> buffer(fileSize); // uint8_t is similar to char
            if(!file.read(reinterpret_cast<char *>(buffer.data()), fileSize)) {
                throw std::runtime_error("There was an error while reading the file");
            }

            if(verbose) {
                std::cout << "Contents of the file: " << std::endl;
                for(auto ch : buffer) {
                    std::cout << ch;
                }
                std::cout << std::endl;
            }

            file.close();
            return buffer;
        }
        else {
            throw std::runtime_error("Unable to open file " + filePath);
        }
    }

} // LZW