#include <iostream>
#include <iomanip>
#include <string>
#include <chrono>

#include "algorithms/naive.hpp"
#include "algorithms/rabin_karp.hpp"


const int TESTS = 1024;

std::string text;
std::string pattern;


template<typename FuncType>
void calcTime(FuncType func, const std::string &funcName) {
    int result;

    // Measuring time
    auto start = std::chrono::high_resolution_clock::now();

    for (int test = 0; test < TESTS; test++) {
        result = func();
    }

    auto end = std::chrono::high_resolution_clock::now();

    int duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
    float timePerTest = (float) duration / TESTS;

    // Output result
    std::cout << funcName + ": " << result << " ";
    // Output time
    std::cout << "[" << duration << " mcs, " << TESTS << " tests, ";
    std::cout << std::setprecision(3) << timePerTest << " mcs per test]" << std::endl;
}


int main() {
    std::cout << std::fixed;

    std::cout << "Type str: ";
    std::cin >> text;

    std::cout << "Type pattern you want to find: ";
    std::cin >> pattern;

    calcTime([](){return naive(text, pattern);}, "Naive");
//    calcTime([](){return horspool(text, pattern);}, "Horspool");
    calcTime([](){return rabinKarp(text, pattern);}, "Rabin-Karp");

    return 0;
}
