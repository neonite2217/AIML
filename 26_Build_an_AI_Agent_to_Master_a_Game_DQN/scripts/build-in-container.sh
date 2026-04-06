#!/bin/bash
# Build and run DQN in a container

set -e

echo "Building DQN Game Agent in container..."

# Create a temporary build script
cat > /tmp/build-dqn.sh << 'EOF'
#!/bin/bash
set -e

# Install dependencies
dnf install -y gcc-c++ cmake make curl unzip python3 python3-pip

# Download LibTorch
cd /workspace
curl -L -o libtorch.zip "https://download.pytorch.org/libtorch/cpu/libtorch-shared-with-deps-2.6.0%2Bcpu.zip"
unzip -q libtorch.zip

# Build project
mkdir -p build
cd build
cmake -DCMAKE_PREFIX_PATH="/workspace/libtorch" ..
cmake --build .

# Run the agent
./dqn
EOF

chmod +x /tmp/build-dqn.sh

# Run in container
podman run --rm -v /var/home/ansh/Projects/super_30/26_Build_an_AI_Agent_to_Master_a_Game_DQN:/workspace:Z -v /tmp/build-dqn.sh:/build-dqn.sh:Z fedora:latest /build-dqn.sh
