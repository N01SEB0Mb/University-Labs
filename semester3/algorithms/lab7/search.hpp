#include <deque>
#include <vector>
#include <string>

// Hash constants
const int P = 567; // Multiplier
const int Q = 5059; // Module


std::pair<int, int> rabin_karp(const std::vector<std::vector<char>> &text,
                               const std::vector<std::vector<char>> &pattern) {
    // Save sizes
    const int heightText = text.size();
    const int widthText = text[0].size();

    const int heightPattern = pattern.size();
    const int widthPattern = pattern[0].size();

    // If pattern sizes bigger than text, then return negative result
    if (widthPattern > widthText || heightPattern > heightText) {
        return std::make_pair(-1, -1);
    }

    // Calculate max multipliers (mod power)
    int maxP = 1;

    for (int index = 0; index < widthPattern - 1; index++) {
        maxP = (maxP * P) % Q;
    }

    // Calculate hashes (different hashes for each row)
    std::vector<int> hashCurr(heightPattern);
    std::vector<int> hashPattern(heightPattern);

    for (int row = 0; row < heightPattern; row++) {
        for (int column = 0; column < widthPattern; column++) {
            hashCurr[row] = (P * hashCurr[row] + text[row][column]) % Q;
            hashPattern[row] = (P * hashPattern[row] + pattern[row][column]) % Q;
        }
    }

    // Iterate possible entries
    for (int row = 0; row <= heightText - heightPattern; row++) {
        for (int column = 0; column <= widthText - widthPattern; column++) {
            // If hashes are equal, then check strings equality
            if (hashCurr == hashPattern) {
                bool found = true;

                for (int i = 0; i < heightPattern; i++) {
                    for (int j = 0; j < widthPattern; j++) {
                        // Check if any of char is not equal

                        if (text[row + i][column + j] != pattern[i][j]) {
                            found = false;
                            break;
                        }
                    }
                }

                // If all of chars are equal, return entry index
                if (found) {
                    return std::make_pair(column, row);
                }
            }

            // Shift right
            if (column < widthText - widthPattern) {
                for (int i = 0; i < heightPattern; i++) {
                    hashCurr[i] = (P * (hashCurr[i] - text[row + i][column] * maxP) + text[row + i][column + widthPattern]) % Q;

                    if (hashCurr[i] < 0) {
                        hashCurr[i] += Q;
                    }
                }
            }
        }

        // Shift down
        if (row < heightText - heightPattern) {
            for (int i = 0; i < heightPattern; i++) {
                hashCurr[i] = 0;

                for (int j = 0; j < widthPattern; j++) {
                    hashCurr[i] = (P * hashCurr[i] + text[i + 1][j]) % Q;
                }
            }
        }
    }

    // If none of entries are matching
    return std::make_pair(-1, -1);
}
