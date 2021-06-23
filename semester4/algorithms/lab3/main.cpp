#define SEPARATORS 16

#include <iostream>

#include "structure/splay_tree.hpp"


void print_separator(const std::string& text, const std::string& value) {
    for (int separator = 0; separator < SEPARATORS; ++separator) {
        std::cout << "-";
    }

    std::cout << std::endl << text;

    if (!value.empty()) {
        std::cout << " (" << value << "):";
    }

    std::cout << std::endl;
}


int main() {
    auto* splay_tree = new structures::SplayTree<int>;

    std::string values[10] = {
            "OOP",
            "Algorithms",
            "Discrete Math",
            "Philosophy",
            "WEB",
            "Culture",
            "Math Analysis",
            "Theory of Algo",
            "Linear Algebra",
            "Physics"
    };
    std::string get_value;

    // Insert values into tree

    for (auto &value: values) {
        splay_tree->insert(value);

        print_separator("Insertion", value);

        splay_tree->output();
    }

    // Get values from tree

//    for (int value = 0; value < 5; ++value) {
//        print_separator("Enter element to get:", "");
//
//        std::cin >> get_value;
//
//        print_separator("Getting", get_value);
//
//        splay_tree->get(get_value);
//        splay_tree->output();
//    }

    // Delete values from tree

    for (auto &value: values) {
        print_separator("Deleting", value);

        splay_tree->erase(value);
        splay_tree->output();
    }

    return 0;
}
