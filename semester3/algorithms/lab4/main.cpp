#include <vector>
#include <utility>
#include <iostream>

#include "algorithms/stable_linear.hpp"
#include "algorithms/stable_nomemory.hpp"
#include "algorithms/linear_nomemory.hpp"


void writeVector(const std::vector<std::pair<int, bool>> &array, const std::string &prompt) {
    std::cout << prompt << std::endl;

    for (auto value: array) {
        std::cout << value.first << " ";
    }

    std::cout << std::endl;

    for (auto value: array) {
        std::cout << value.second << " ";
    }

    std::cout << std::endl;
}


int main() {
    // Read size
    int n;
    std::cin >> n;

    // Init vector
    std::vector<std::pair<int, bool>> array(n);

    // Read vector
    int number;
    bool key;

    for (int row = 0; row < n; row++) {
        // Read value
        std::cin >> number >> key;
        // Add value
        array[row] = std::make_pair(number, key);
    }

    // 1 & 2
    writeVector(stable_linear(array), "1 & 2:");
    std::cout << std::endl;

    // 1 & 3
    writeVector(linear_nomemory(array), "1 & 3:");
    std::cout << std::endl;

    // 2 & 3
    writeVector(stable_nomemory(array), "2 & 3:");
    std::cout << std::endl;

    return 0;
}
