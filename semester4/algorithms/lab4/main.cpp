#include <iostream>

#include "structure/optimal_bst.hpp"


int main() {
    const std::vector<std::string> values = {
            "OOP",
            "WEB",
            "Algorithms",
            "Math Analysis",
            "Philosophy",
            "Theory of Algorithms",
            "Discrete Math",
            "Culture",
            "Physics",
            "Linear Algebra"
    };
    std::vector<double> probabilities = {0.1, 0.07, 0.11, 0.04, 0.06, 0.05, 0.08, 0.03, 0.12, 0.06};
    std::vector<double> fict_probabilities = {0.1, 0.07, 0.11, 0.04, 0.06, 0.05, 0.08, 0.03, 0.12, 0.06};

    // Create and output tree

    auto* optimal_bst_tree = new structures::OptimalBST(values, probabilities, fict_probabilities);

    print_separator("Ivanov Ivan Ivanovych:");

    optimal_bst_tree->output();
}
