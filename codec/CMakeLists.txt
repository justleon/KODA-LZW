cmake_minimum_required(VERSION 3.23)
project(KODA_LZW)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "$<0:>${PROJECT_SOURCE_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "$<0:>${PROJECT_SOURCE_DIR}/lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "$<0:>${PROJECT_SOURCE_DIR}/lib")

include_directories(include)

add_library(Codec_lzw SHARED
        src/codec_lzw.cpp
)