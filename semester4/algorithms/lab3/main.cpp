#define SEPARATORS 16

#include <iostream>

#include "structure/splay_tree.hpp"


void print_separator(const std::string& text, const int* value = nullptr) {
    for (int separator = 0; separator < SEPARATORS; ++separator) {
        std::cout << "-";
    }

    std::cout << std::endl << text;

    if (value) {
        std::cout << " (" << *value << "):";
    }

    std::cout << std::endl;
}


int main() {
    auto* splay_tree = new structures::SplayTree<int>;

    int values[10] = {10, 9, 1, 5, 7, 2, 6, 3, 4, 8};
    int get_value;

    // Insert values into tree

    for (int &value: values) {
        splay_tree->insert(value);

        print_separator("Insertion", &value);

        splay_tree->output();
    }

    // Get values from tree

    for (int value = 0; value < 5; ++value) {
        print_separator("Enter element to get:");

        std::cin >> get_value;

        print_separator("Getting", &get_value);

        splay_tree->get(get_value);
        splay_tree->output();
    }

    // Delete values from tree

    for (int i = 1; i <= 10; ++i) {
        print_separator("Deleting", &i);

        splay_tree->erase(i);
        splay_tree->output();
    }

    return 0;
}
