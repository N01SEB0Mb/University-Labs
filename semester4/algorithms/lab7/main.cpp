#include <iostream>

#include "structure/binomial_heap.hpp"


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
    auto* binomial_heap = new structures::BinomialHeap<int>();

    int values[10] = {5, 8, 7, 1, 4, 2, 6, 9, 3};

    // Insert values

    for (auto &value: values) {
        print_separator("Insert", &value);

        binomial_heap->insert(value);
        binomial_heap->output();
    }

    // Decrease key

    print_separator("Decrease key (5-th -> -2)");

    binomial_heap->decreaseKey(5, -2);
    binomial_heap->output();

    // Delete

    print_separator("Delete (2-th)");

    binomial_heap->erase(2);
    binomial_heap->output();

    // Extract min x9

    for (int value = 0; value < 9; ++value) {
        print_separator("Extract min");

        binomial_heap->extractMin();
        binomial_heap->output();
    }

    return 0;
}
