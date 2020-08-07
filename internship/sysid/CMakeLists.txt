 cmake_minimum_required(VERSION 3.8)

 set(This SysId)

 project(${This} C CXX)

 set(CMAKE_C_STANDARD 99)
 set(CMAKE_CXX_STANDARD 17)
 
 enable_testing()

 add_subdirectory(googletest)

 set(Headers
    SysId.hpp
 )

 set(Sources
    SysId.cpp
 )

 add_library(${This} STATIC ${Sources} ${Headers})

 add_subdirectory(test)