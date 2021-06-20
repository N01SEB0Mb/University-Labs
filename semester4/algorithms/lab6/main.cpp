#include <iostream>

#include "structure/b_plus_tree.hpp"


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


void print_separator(const std::string& text, const std::string& value) {
    for (int separator = 0; separator < SEPARATORS; ++separator) {
        std::cout << "-";
    }

    std::cout << std::endl << text << " (" << value << "):";
    std::cout << std::endl;
}


int main() {
    auto* tree = new structures::BPlusTree<int, int>(2);

    int numbers[10] = {6, 9, 11, 5, 4, 7, 3, 1, 2, 8};

    // Insert

    for (int &key: numbers) {
        tree->insert(key, 0);

        print_separator("Insert", &key);

        tree->output();
    }

    tree->insert(10, 3);

    print_separator("Insert", "10, 3");

    tree->output();

    // Search

    print_separator("Search by key", "4");
    std::cout << tree->search(4) << std::endl;

    print_separator("Search by key", "8");
    std::cout << tree->search(8) << std::endl;

    print_separator("Search by key", "10");
    std::cout << tree->search(10) << std::endl;

    // Delete

    for (int i = 1; i <= 11; i++) {
        tree->erase(i);

        print_separator("Delete", &i);

        tree->output();
    }

    print_separator("");

    return 0;
}
