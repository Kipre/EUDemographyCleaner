 cmake_minimum_required(VERSION 3.8)

 set(This SysIdTests)

 set(Sources
    SysIdTests.cpp
)

add_compile_options(/MDd)

add_executable(${This} ${Sources})
target_link_libraries(${This} PUBLIC
    gtest_main
    gmock_main
    SysId
)

add_test(
    NAME ${This}
    COMMAND ${This}
)