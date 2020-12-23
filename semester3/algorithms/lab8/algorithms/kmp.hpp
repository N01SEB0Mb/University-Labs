#include <string>
#include <vector>


std::vector<int> prefix(const std::string& a) {
    std::vector<int> result;

    result.emplace_back(0);
    int k;

    for (int i = 1; i < a.length(); i++) {
        k = result[i - 1];

        while (true) {
            if (a[i] == a[k]) {
                result.emplace_back(k + 1);
                break;
            }
            else if (k == 0) {
                result.emplace_back(0);
                break;
            }
            else {
                k = result[k];
            }
        }
    }

    return result;
}

int kmp(std::string& text, std::string& pattern){
    std::vector<int> prefixes = prefix(pattern);

    std::string b_copy = text + text;
    int q = 0;

    for (int i = 0; i < b_copy.length(); i++){
        while (q > 0 && pattern[q] != b_copy[i]){

            q = prefixes[q];

        }
        if (pattern[q] == b_copy[i])
            q = q + 1;
        if (q == pattern.length())
            return i - pattern.length() + 1;

    }

    return -1;
}
