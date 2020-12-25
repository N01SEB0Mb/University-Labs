#include <iostream>

#include "functions.hpp"


int main() {
    // Input parameters
    std::cout << "Type number of nodes: ";
    std::cin >> n;

    std::cout << "Type power: ";
    std::cin >> d;

    // Input heap
    std::cout << "Type heap: ";
    int value;

    for (int node = 0; node < n; node++) {
        std::cin >> value;
        heap.push_back(value);
    }

    buildHeap();

    bool finished = false;
    int operation;

    while (!finished) {
        std::cout << "Choose operation:\n"
                     "1 - Extract Max\n"
                     "2 - Insert\n"
                     "3 - Increase Key\n"
                     "4 - Get height\n"
                     "5 - Print heap\n"
                     "0 - Exit\n";

        std::cin >> operation;
        std::cout << "----------------" << std::endl;

        switch (operation) {
            case 1:
                std::cout << extractMax() << std::endl;
                break;
            case 2:
                break;
            case 3:
                break;
            case 4:
                std::cout << height() << std::endl;
            case 5:
                writeHeap();
                break;
            case 0:
                finished = true;
                std::cout << "Exit..." << std::endl;
                break;
            default:
                std::cout << "Unknown operation, try again" << std::endl;
                break;
        }

        std::cout << "----------------" << std::endl;
    }
    // Choose operation


    return 0;
}
