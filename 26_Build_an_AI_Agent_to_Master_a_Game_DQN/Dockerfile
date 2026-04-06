# Dockerfile for building DQN Game Agent
FROM fedora:latest

# Install build dependencies
RUN dnf install -y gcc-c++ cmake make python3 python3-pip && \
    dnf clean all

# Install PyTorch (which includes LibTorch cmake files)
RUN pip3 install torch --no-cache-dir

# Set working directory
WORKDIR /workspace

# Copy project files
COPY . /workspace/

# Build the project
RUN mkdir -p build && cd build && \
    cmake -DCMAKE_PREFIX_PATH="$(python3 -c 'import torch; print(torch.utils.cmake_prefix_path)')" .. && \
    cmake --build .

# Set the entrypoint
CMD ["./build/dqn"]
