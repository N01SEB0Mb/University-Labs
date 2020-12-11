#include "iostream"

#include "shifted.hpp"


int main() {
    std::string input;
    std::string output;

    // Input origin string
    std::cout << "Type origin string:  ";
    std::cin >> input;

    // Input shifted string
    std::cout << "Type shifted string: ";
    std::cin >> output;

    // Output value
    std::cout << isShifted(input, output) << std::endl;
}
