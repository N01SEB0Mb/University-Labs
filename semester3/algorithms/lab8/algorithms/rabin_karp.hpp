#include <string>

// Hash constants
const int P = 101; // Multiplier
const int Q = 127; // Module


int rabinKarp(const std::string &text, const std::string &pattern) {
    // Save length
    const int lenText = text.length();
    const int lenPattern = pattern.length();

    // Check if pattern < text
    if (lenPattern > lenText) {
        return -1;
    }

    // Hash variables
    int hashCurr = 0;
    int hashPattern = 0;

    // Calculate pattern and first entry
    for (int index = 0; index < lenPattern; index++) {
        hashCurr = (P * hashCurr + text[index]) % Q;
        hashPattern = (P * hashPattern + pattern[index]) % Q;
    }

    // Calculate first multiplier (mod power)
    int maxP = 1;

    for (int index = 0; index < lenPattern - 1; index++) {
        maxP = (maxP * P) % Q;
    }

    // Iterate possible entries
    for (int current = 0; current <= lenText - lenPattern; current++) {
        // If hashes are equal, then check strings equality
        if (hashCurr == hashPattern) {
            bool found = true;

            for (int index = 0; index < lenPattern; index++) {
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

        // If entry is not last
        if (current < lenText - lenPattern) {
            // Roll hash (remove old char, shift, add new char)
            hashCurr = (P * (hashCurr - text[current] * maxP) + text[current + lenPattern]) % Q;

            // If hash is negative
            if (hashCurr < 0) {
                hashCurr += Q;
            }
        }
    }

    // If none of entries are matching
    return -1;
}
