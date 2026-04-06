cmake_minimum_required(VERSION 3.10)
project(DQN_Game)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find and configure LibTorch
# You need to download LibTorch and set the CMAKE_PREFIX_PATH
# e.g. export CMAKE_PREFIX_PATH=/path/to/libtorch
find_package(Torch REQUIRED)

add_executable(dqn dqn.cpp)
target_link_libraries(dqn "${TORCH_LIBRARIES}")
set_property(TARGET dqn PROPERTY CXX_STANDARD 14)
set_property(TARGET dqn PROPERTY CXX_STANDARD 17)
