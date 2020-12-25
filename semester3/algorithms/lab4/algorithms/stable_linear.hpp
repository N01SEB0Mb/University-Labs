#include <vector>
#include <utility>


std::vector<std::pair<int, bool>> stable_linear(std::vector<std::pair<int, bool>> &array) {
    std::vector<std::pair<int, bool>> result;

    for (auto &value: array) {
        if (!value.second) {
            result.push_back(value);
        }
    }

    for (auto &value: array) {
        if (value.second) {
            result.push_back(value);
        }
    }

    return result;
}
