#include <cmath>
#include <string>
#include <iostream>


const int q = 127;
const int x = 101;


int rabin_karp(const std::string &text, const std::string &pattern) {
    int n = text.length(), m = pattern.length();

    if (m > n) {
        return -1;
    }

    int p = 0;
    int t = 0;
    int h = 1;

    for (int i = 0; i < m - 1; i++)
        h = (h * x) % q;

    for (int i = 0; i < m; i++) {
        p = (x * p + pattern[i]) % q;
        t = (x * t + text[i]) % q;
    }

    for (int i = 0; i <= n - m; i++) {
        if (p == t) {
            bool found = true;

            for (int j = 0; j < m; j++) {
                if (text[i + j] != pattern[j]) {
                    found = false;
                    break;
                }
            }

            if (found) {
                return i;
            }
        }

        if (i < n - m) {
            t = (x * (t - text[i] * h) + text[i + m]) % q;

            if (t < 0) {
                t += q;
            }
        }
    }

    return -1;
}
