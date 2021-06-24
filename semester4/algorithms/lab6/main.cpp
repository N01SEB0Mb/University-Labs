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

    std::vector<std::string> professors = {
            "Ivanov I. I.",
            "Borisov B. B.",
            "Foobar F. B.",
            "Olexandrov O. O.",
            "Nikolaev N. N."
    };
    std::vector<std::vector<std::string>> professor_courses = {
            {"OOP", "Algorithms"},
            {"Linear Algebra"},
            {},
            {"Math Analysis", "Discrete Math", "Linear Algebra"},
            {"Philosophy", "Physics"}
    };

    // Insert

    for (int i = 0; i < 5; ++i) {
        tree->insert(professors[i], professor_courses[i]);

        print_separator("Insert", professors[i]);

        for (auto &courses: professor_courses[i]) {
            std::cout << courses << std::endl;
        }


        tree->output();
    }

    // Insert one value

    std::string name = "Test N. T.";
    std::vector<std::string> courses = {"Theory of Algorithms"};

    tree->insert(name, courses);

    print_separator("Insert", "Test N. T., {'Theory of Algorithms'}");

    tree->output();

    // Search

    std::vector<std::string> search_names = {"Ivanov I. I.", "Borisov B. B."};

    for (auto &search_name: search_names) {
        print_separator("Search by key", search_name);

        auto found_courses = tree->search(search_name);

        for (auto &found_course: found_courses) {
            std::cout << found_course << " " << std::endl;
        }
    }

    // Delete

    for (int i = 0; i < 3; ++i) {
        tree->erase(professors[i]);

        print_separator("Delete", professors[i]);

        tree->output();
    }

    print_separator("");

    return 0;
}
