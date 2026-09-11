cmake_minimum_required(VERSION 3.16)

project(BiteWireUpdater)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

qt_standard_project_setup()

qt_add_executable(BiteWireUpdater
    main.cpp
    updater_ui.cpp
    updater_logic.cpp
)

target_link_libraries(BiteWireUpdater PRIVATE
    Qt6::Widgets
)
