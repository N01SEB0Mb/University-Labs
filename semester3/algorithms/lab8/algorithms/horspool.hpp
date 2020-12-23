#include <map>
#include <string>


int horspool(const std::string& text, const std::string& pattern) {
    std::map<char, int> shifts;

    for (char i: text){
        shifts[i] = pattern.size();
    }

    for (int i = 0; i < pattern.size() - 1; i++) {
        shifts[pattern[i]] = pattern.size() - i - 1;
    }

    int k;
    int i = pattern.size() - 1;

    while (i < text.size()) {
        for (k = 0; k < pattern.size() && pattern[pattern.size() - k - 1] == text[i - k]; k++);

        if (k == pattern.size())
            return i - pattern.size() + 1;
        else
            i += shifts[text[i]];
    }

    return -1;
}
