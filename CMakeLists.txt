cmake_minimum_required(VERSION 3.23)
project(KODA_LZW)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(KODA_LZW
        main.cpp
        codec_src/Codec.cpp)
