//
// LZW Codec
// WUT project for Data Compression
// Created on 16.11.2022.
//

#include <valarray>
#include "Codec.h"
#include <stdexcept>

namespace LZW {

#pragma region Codec
    //TODO: In current form this is very basic implementation (needs more universal form)
    //Maybe implement it on templates?
    void Codec::Coder(std::string& filePath, int dictBitSize) {
        if (dictBitSize >= 33) {
            throw std::out_of_range("Dictionary index bit size can't be bigger than 32");
        }

        std::map<std::basic_string<uint8_t>, int> table;
        uint32_t maxDictSize = pow(2, dictBitSize);
        for(int i = 0; i < 256; i++) {
            std::basic_string<uint8_t> record {};
            record += uint8_t(i);
            table[record] = i;
        }

        std::vector<uint8_t> inputBuffer = ReadFile(filePath);
        std::vector<uint32_t> output;
        std::basic_string<uint8_t> p, c;
        p = inputBuffer[0];
        int index = 1, recordCount = 256;

        while (index < inputBuffer.size()) {
            c = inputBuffer[index];
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
        output.push_back(table[p]);
    }

#pragma endregion

    std::basic_string<uint8_t> Codec::Decoder(std::string &filePath, int dictBitSize) {
        if (dictBitSize >= 33) {
            throw std::out_of_range("Dictionary index bit size can't be bigger than 32");
        }
        uint32_t maxDictSize = pow(2, dictBitSize);
        // Build the dictionary.
        int dictSize = 256;
        std::map<uint32_t, std::basic_string<uint8_t>> dictionary;
        for (int i = 0; i < 256; i++){
            dictionary[i] = std::basic_string<uint8_t>(1, i);
        }

        //TODO Add read uint32 format
        std::vector<uint32_t> inputBuffer = {};//ReadFile(filePath);

        std::basic_string<uint8_t> w(1, inputBuffer[0]);
        std::basic_string<uint8_t> result = w;
        std::basic_string<uint8_t> entry;
        for (int index = 1; index < inputBuffer.size(); ++index) {
            uint32_t k = inputBuffer[index];
            if (dictionary.count(k))
                entry = dictionary[k];
            else if (k == dictSize)
                entry = w + w[0];
            else
                throw std::runtime_error("Bad compressed k");

            result += entry;

            // Add w+entry[0] to the dictionary.
            dictionary[dictSize++] = w + entry[0];

            w = entry;
        }
        return result;
    }

#pragma region I/O

    std::vector<uint8_t> Codec::ReadFile(std::string filePath, bool verbose) {
        std::ifstream file(filePath, std::ios::binary);
        if (file) {
            std::streampos begOfFile, endOfFile;
            file.seekg(0, std::ios::end);
            endOfFile = file.tellg();
            file.seekg(0, std::ios::beg);
            begOfFile = file.tellg();

            long fileSize = endOfFile - begOfFile;
            std::cout << filePath << " size: " << fileSize << std::endl;
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

    void Codec::WriteFile(std::string fileName) {
        std::ofstream file(fileName + ".lzw", std::ios::binary);
        if(file) {
            //TODO: Implement proper file writing

            std::streampos begOfFile, endOfFile;
            file.seekp(0, std::ios::end);
            endOfFile = file.tellp();
            file.seekp(0, std::ios::beg);
            begOfFile = file.tellp();

            long fileSize = endOfFile - begOfFile;
            std::cout << fileName << " size: " << fileSize << std::endl;
        }
    }
#pragma endregion

} // LZW