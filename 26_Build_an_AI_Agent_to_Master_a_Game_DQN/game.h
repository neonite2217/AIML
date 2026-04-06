#pragma once
#include <vector>
#include <random>
#include <utility>

// A very simple game environment (e.g., a 1D grid world)
class Game {
public:
    Game() : state(0), max_steps(20), steps(0) {}

    std::vector<float> reset() {
        state = 0;
        steps = 0;
        return {static_cast<float>(state)};
    }

    // Returns <next_state, reward, done>
    std::tuple<std::vector<float>, float, bool> step(int action) {
        steps++;
        if (action == 0) { // move left
            state--;
        } else { // move right
            state++;
        }

        float reward = -0.1; // small penalty for each step
        bool done = false;

        if (state == 5) {
            reward = 1.0; // reward for reaching the goal
            done = true;
        } else if (state == -5) {
            reward = -1.0; // penalty for falling off
            done = true;
        } else if (steps >= max_steps) {
            done = true;
        }

        return {{static_cast<float>(state)}, reward, done};
    }

private:
    int state;
    int steps;
    int max_steps;
};
