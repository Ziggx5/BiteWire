cmake_minimum_required(VERSION 3.15)
project(bitewire)
find_package(pybind11 REQUIRED)
pybind11_add_module(bitewire get_directory.cpp)
