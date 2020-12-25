#include <vector>
#include <utility>
#include <iostream>

#include "sort.hpp"


int main() {
    // Input size
    int n;
    std::cout << "Type length of array: ";
    std::cin >> n;

    // Init vectors
    std::vector<int> first(n);
    std::vector<int> second(n);

    std::cout << "Type first array: ";
    for (int index = 0; index < n; index++) {
        std::cin >> first[index];
    }

    std::cout << "Type second array: ";
    for (int index = 0; index < n; index++) {
        std::cin >> second[index];
    }

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
