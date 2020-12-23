#include <iostream>
#include <string>
#include <ctime>

#include "algorithms/kmp.hpp"
#include "algorithms/naive.hpp"
#include "algorithms/horspool.hpp"
#include "algorithms/rabin_karp.hpp"


std::string text;
std::string pattern;


template<typename FuncType>
void calcTime(FuncType func, const std::string &funcName) {
    // Measuring time
    clock_t start = clock();
    int result = func();
    clock_t time = clock() - start;

    // Output result
    std::cout << funcName + "() -> " << result << " ";
    // Output time
    std::cout << "[" << time << " ms]" << std::endl;
}


int main() {
    std::cout << "Type str: ";
    std::cin >> text;

    std::cout << "Type pattern you want to find: ";
    std::cin >> pattern;

    // Testing different algorithms
    calcTime([](){return kmp(text, pattern);}, "KMP");
    calcTime([](){return naive(text, pattern);}, "Naive");
    calcTime([](){return horspool(text, pattern);}, "Horspool");
    calcTime([](){return rabin_karp(text, pattern);}, "Rabin-Karp");
}
