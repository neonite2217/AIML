#include <torch/torch.h>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <vector>
#include <random>
#include "game.h"

// 2. Build Q-network
struct QNetwork : torch::nn::Module {
    QNetwork(int64_t state_size, int64_t action_size) {
        fc1 = register_module("fc1", torch::nn::Linear(state_size, 128));
        fc2 = register_module("fc2", torch::nn::Linear(128, 128));
        fc3 = register_module("fc3", torch::nn::Linear(128, action_size));
    }

    torch::Tensor forward(torch::Tensor x) {
        x = torch::relu(fc1->forward(x));
        x = torch::relu(fc2->forward(x));
        x = fc3->forward(x);
        return x;
    }

    torch::nn::Linear fc1{nullptr}, fc2{nullptr}, fc3{nullptr};
};

// 3. Epsilon-greedy exploration
int select_action(torch::Tensor state, QNetwork& network, double epsilon, int action_size) {
    if (static_cast<double>(rand()) / RAND_MAX < epsilon) {
        return rand() % action_size;
    } else {
        torch::NoGradGuard no_grad;
        return network.forward(state).argmax().item<int>();
    }
}

int main() {
    // Check if CUDA is available
    torch::Device device(torch::kCPU);
    if (torch::cuda::is_available()) {
        std::cout << "CUDA is available! Training on GPU." << std::endl;
        device = torch::kCUDA;
    } else {
        std::cout << "Training on CPU." << std::endl;
    }

    Game env;
    QNetwork model(1, 2);
    model.to(device);
    torch::optim::Adam optimizer(model.parameters(), torch::optim::AdamOptions(1e-3));

    // Simple Replay Buffer
    struct ReplayBuffer {
        std::vector<torch::Tensor> state, next_state;
        std::vector<int> action;
        std::vector<float> reward;
        std::vector<bool> done;
        int capacity = 10000;
        int index = 0;
        
        void push(torch::Tensor s, int a, float r, torch::Tensor ns, bool d) {
            if (state.size() < capacity) {
                state.push_back({});
                action.push_back({});
                reward.push_back({});
                next_state.push_back({});
                done.push_back({});
            }
            state[index] = s;
            action[index] = a;
            reward[index] = r;
            next_state[index] = ns;
            done[index] = d;
            index = (index + 1) % capacity;
        }
    };
    ReplayBuffer memory;

    int episodes = 500;
    int batch_size = 64;
    double gamma = 0.99;
    double epsilon = 1.0;
    double epsilon_min = 0.01;
    double epsilon_decay = 0.995;

    for (int i = 0; i < episodes; ++i) {
        auto state_vec = env.reset();
        torch::Tensor state = torch::tensor(state_vec).to(device);
        bool done = false;
        float total_reward = 0.0f;

        while (!done) {
            int action = select_action(state, model, epsilon, 2);
            auto [next_state_vec, reward, step_done] = env.step(action);
            done = step_done;
            total_reward += reward;

            torch::Tensor next_state = torch::tensor(next_state_vec).to(device);
            memory.push(state, action, reward, next_state, done);
            state = next_state;

            if (memory.state.size() >= batch_size) {
                // Sample a batch from memory
                std::vector<int> indices(batch_size);
                for(int k=0; k<batch_size; ++k) indices[k] = rand() % memory.state.size();
                
                std::vector<torch::Tensor> state_batch, next_state_batch;
                std::vector<int> action_batch;
                std::vector<float> reward_batch;
                std::vector<float> done_batch;

                for(int idx : indices) {
                    state_batch.push_back(memory.state[idx]);
                    next_state_batch.push_back(memory.next_state[idx]);
                    action_batch.push_back(memory.action[idx]);
                    reward_batch.push_back(memory.reward[idx]);
                    done_batch.push_back(memory.done[idx] ? 1.0f : 0.0f);
                }

                auto states = torch::stack(state_batch);
                auto next_states = torch::stack(next_state_batch);
                auto actions = torch::tensor(action_batch, torch::TensorOptions().dtype(torch::kLong)).to(device);
                auto rewards = torch::tensor(reward_batch, torch::TensorOptions().dtype(torch::kFloat32)).to(device);
                auto dones = torch::tensor(done_batch, torch::TensorOptions().dtype(torch::kFloat32)).to(device);
                
                auto q_values = model.forward(states).gather(1, actions.unsqueeze(1));
                auto next_q_values = std::get<0>(model.forward(next_states).max(1)).detach();
                auto expected_q_values = rewards + gamma * next_q_values * (1.0 - dones);
                
                auto loss = torch::mse_loss(q_values, expected_q_values.unsqueeze(1));

                optimizer.zero_grad();
                loss.backward();
                optimizer.step();
            }
        }
        epsilon = std::max(epsilon_min, epsilon * epsilon_decay);

        if (i % 20 == 0) {
            std::cout << "Episode " << i << ", Total Reward: " << total_reward << ", Epsilon: " << epsilon << std::endl;
        }
    }

    // Save the model
    torch::serialize::OutputArchive archive;
    model.save(archive);
    archive.save_to("dqn_model.pt");
    std::cout << "Training finished and model saved." << std::endl;

    return 0;
}
