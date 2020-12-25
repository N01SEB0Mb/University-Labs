#include <vector>
#include <utility>


std::vector<std::pair<int, bool>> stable_nomemory(std::vector<std::pair<int, bool>> &array) {
    for (int index = 1; index < array.size(); index++) {
        std::pair<int, bool> current = array[index];

        int next;

        for (next = index; next > 0 && array[next - 1].second > current.second; next--) {
            array[next] = array[next - 1];
        }

        array[next] = current;
    }

    return array;
}
