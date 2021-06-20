#include <iostream>

#include "structure/optimal_bst.hpp"


int main() {
    std::vector<int> values;
    std::vector<double> probabilities;
    std::vector<double> fict_probabilities;

    // Fill vectors

    for (int value = 0; value < 8; ++value) {
        values.push_back(value + 1);
        probabilities.push_back(0.05);
        fict_probabilities.push_back(0.05);
    }

    // Create and output tree

    auto* optimal_bst_tree = new structures::OptimalBST(values, probabilities, fict_probabilities);

    print_separator("Tree:");

    optimal_bst_tree->output();
}
