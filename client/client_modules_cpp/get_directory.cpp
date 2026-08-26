#include <iostream>
#include <filesystem>
#include <cstdlib>
#include <pybind11/pybind11.h>

std::string getAppDataPath() {
    std::string user_directory;
#if defined(__linux__)
    user_directory = std::string(getenv("HOME")) + "/.local/share/bitewire";
#elif defined(_WIN32)
    user_directory = std::string(getenv("APPDATA")) + "\\bitewire";
#endif
    std::filesystem::create_directories(user_directory);
    return user_directory;
}

PYBIND11_MODULE(bitewire, handle) {
    handle.doc() = "Get app data path,";
    handle.def("get_app_data_path", &getAppDataPath);
}
