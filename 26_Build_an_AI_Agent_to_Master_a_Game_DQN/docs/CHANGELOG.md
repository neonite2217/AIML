# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure with C++ DQN implementation
- Game environment (1D grid world) in `game.h`
- DQN agent implementation in `dqn.cpp`
- CMake build configuration
- Complete documentation suite (README, architecture, tech stack, SDLC)
- Setup script for automated build

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Removed
- N/A (initial release)

## [1.0.0] - 2026-03-14

### Added
- Initial release of DQN Game Agent
- Deep Q-Network implementation using LibTorch
- Epsilon-greedy exploration strategy
- Experience replay buffer
- Training loop with 500 episodes
- Model saving functionality
- Console output showing learning progress
