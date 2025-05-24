cmake_minimum_required(VERSION 4.0)
project(ForeFlightCodeChallenge)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(nlohmann_json REQUIRED)

add_executable(${PROJECT_NAME} src/FlightInfo.cpp)
target_link_libraries(${PROJECT_NAME} nlohmann_json::nlohmann_json)
