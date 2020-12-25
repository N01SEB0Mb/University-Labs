#include <vector>
#include <utility>


std::vector<std::pair<int, bool>> linear_nomemory(std::vector<std::pair<int, bool>> array) {
    int counter = 0;

    for (auto &value: array) {
        if (!value.second) {
            counter++;
        }
    }

    int first = 0;
    int last = (int) array.size() - 1;


    while (first < counter) {
        while (!array[first].second && first < counter) {
            first++;
        }

        if (first < counter) {
            while (array[last].second) {
                last--;
            }

            std::swap(array[first], array[last]);

            first++;
            last--;
        }
    }

    return array;
}
