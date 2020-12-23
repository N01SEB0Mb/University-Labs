#include "string"


int naive(const std::string& text, const std::string& pattern) {
    bool found;

    for (int i = 0; i < text.size(); i++) {
        found = true;

        for (int j = 0; j < pattern.size(); j++) {
            if (pattern[j] != text[i + j]) {
                found = false;
            }
        }

        if (found) {
            return i;
        }
    }

    return -1;
}
