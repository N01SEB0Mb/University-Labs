#include <vector>
#include <utility>
#include <string>
#include <iostream>

#include "search.hpp"


void readVector(std::vector<std::vector<char>> &var, const std::string &prompt) {
    // Write prompt
    std::cout << prompt << std::endl;

    // Init input variable
    std::string textRow;

    // Input until empty line
    while (std::getline(std::cin, textRow) && !textRow.empty())
    {
        std::vector<char> row;

        for (auto symbol: textRow) {
            row.push_back(symbol);
        }

        var.push_back(row);
    }
}


int main() {
    // Init vectors
    std::vector<std::vector<char>> text;
    std::vector<std::vector<char>> pattern;

    // Input
    readVector(text, "Type text (empty line to end):");
    readVector(pattern, "Type text (empty line to end):");

    // Get and output result
    std::pair<int, int> result = rabin_karp(text, pattern);
    std::cout << result.first << " " << result.second << std::endl;
}
