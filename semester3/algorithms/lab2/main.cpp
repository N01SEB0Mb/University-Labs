#include <vector>
#include <utility>
#include <algorithm>
#include <random>
#include <iostream>

#include "sort.hpp"


std::vector<int> getRandom(const int &size) {
    std::vector<int> result(size);

    for (int i = 0; i < size; i++) {
        result.push_back(rand() % 255);
    }

    return result;
}


int main() {
    // Input size
    int n;
    std::cout << "Type length of array: ";
    std::cin >> n;

    // Init vectors
    std::vector<int> first(n);
    std::vector<int> second(n);

    first = getRandom(n);
    second = first;
    auto rng = std::default_random_engine {};
    std::shuffle(first.begin(), first.end(), rng);

    // Output vectors
    for (int value: first) {
        std::cout << value << " ";
    }

    std::cout << std::endl;

    for (int value: second) {
        std::cout << value << " ";
    }

    std::cout << std::endl;

    // Sort vector
    std::pair<std::vector<int>, std::vector<int>> result = sort(first, second);

    // Output vectors
    for (int value: result.first) {
        std::cout << value << " ";
    }

    std::cout << std::endl;

    for (int value: result.second) {
        std::cout << value << " ";
    }

    return 0;
}
