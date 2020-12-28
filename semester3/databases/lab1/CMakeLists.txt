cmake_minimum_required(VERSION 3.17)
project(databases C)

set(CMAKE_C_STANDARD 99)

add_executable(databases main.c database.h database.c)
