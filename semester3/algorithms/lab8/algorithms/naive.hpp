#include <string>


int naive(const std::string& text, const std::string& pattern) {
    bool found;

    // Iterate possible entries
    for (int current = 0; current < text.size(); current++) {
        found = true;

        for (int index = 0; index < pattern.size(); index++) {
            // Check if any of char is not equal

            if (text[current + index] != pattern[index]) {
                found = false;
                break;
            }
        }

        // If all of chars are equal, return entry index
        if (found) {
            return current;
        }
    }

    // If none of entries are matching
    return -1;
}
