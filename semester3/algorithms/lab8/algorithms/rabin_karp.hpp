#include <string>
#include <cmath>

const int q = 997;
const int size = 100;


int hash(const std::string& a) {
    int res = 0;

    for (int i = 0; i < a.size(); i++) {
        res = (res * size + int(a[i])) % q;
    }

    return res;
}

bool check(const std::string& text, const std::string& pattern,
           const int& hpattern, const int& htext,
           const int& shift) {

    if(hpattern != htext)
        return false;

    for (int i = 0; i < pattern.size(); i++) {
        if (pattern[i] != text[shift + i]) {
            return false;
        }
    }

    return true;
}


int rabin_karp(const std::string& text, const std::string& pattern){
    int h = pow(size, pattern.size() - 1);
    int htext;
    int hpattern = hash(pattern);

    std::string temp;

    for (int j = 0; j < pattern.size(); j++) {
        temp += text[j];
    }

    htext = hash(temp);

    for (int i = 0; i < text.size() - pattern.size() + 1; i++) {
        if (check(text, pattern, hpattern, htext, i)) {
            return i;
        }
        else {
            htext = ((htext + int(text[i]) * (q - h % q)) * size + int(text[i + pattern.size()])) % q;
        }
    }

    return -1;
}
