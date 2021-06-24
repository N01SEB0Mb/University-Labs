#include <iostream>

#include "structure/binomial_heap.hpp"


void print_separator(const std::string& text, const std::string &value) {
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
    auto* binomial_heap = new structures::BinomialHeap<int>();

    std::vector<std::string> courses = {
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

    // Insert values

    for (auto &course: courses) {
        print_separator("Insert", course);

        binomial_heap->insert(course);
        binomial_heap->output();
    }

    // Delete

    print_separator("Delete", "OOP");

    binomial_heap->erase(2);
    binomial_heap->output();

    // Extract min x9

    for (int value = 0; value < 9; ++value) {
        print_separator("Extract min", "");

        binomial_heap->extractMin();
        binomial_heap->output();
    }

    return 0;
}
