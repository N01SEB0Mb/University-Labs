#include <vector>
#include <utility>


std::pair<std::vector<int>, std::vector<int>> sort(std::vector<int> &first,
                                                        std::vector<int> &second) {
    // Check if array has 2 or more elements
    if (first.size() <= 1) {
        return std::make_pair(first, second);
    }

    int pivot = first[0];

    // Second array partition
    std::vector<int> lessSecond, equal, greaterSecond;

    for (int value: second) {
        if (value > pivot) {
            greaterSecond.push_back(value);
        }
        else if (value < pivot) {
            lessSecond.push_back(value);
        }
        else {
            equal.push_back(value);
        }
    }

    // First array partition
    pivot = equal[0];
    std::vector<int> lessFirst, greaterFirst;

    for (int value: first) {
        if (value > pivot) {
            greaterFirst.push_back(value);
        }
        else if (value < pivot) {
            lessFirst.push_back(value);
        }
    }

    // Bidlocode
    std::pair<std::vector<int>, std::vector<int>> less = sort(lessFirst, lessSecond);
    std::pair<std::vector<int>, std::vector<int>> greater = sort(greaterFirst, greaterSecond);

    less.first.insert(less.first.end(), equal.begin(), equal.end());
    less.first.insert(less.first.end(), greater.first.begin(), greater.first.end());

    less.second.insert(less.second.end(), equal.begin(), equal.end());
    less.second.insert(less.second.end(), greater.second.begin(), greater.second.end());

    return less;
}
