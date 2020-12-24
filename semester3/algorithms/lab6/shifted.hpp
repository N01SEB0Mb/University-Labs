#include <string>

// Hash constants
const int32_t P = 255;
const int32_t Q = INT32_MAX / 2 - 1;


int isShifted(const std::string &origin,
              const std::string &shifted) {
    // Save length
    const int len = origin.length();

    // If length not matches
    if (len != shifted.length()) {
        return -1;
    }

    // Hash variables
    int32_t hashOrigin = 0;
    int32_t hashShifted = 0;

    // Calculate pattern and first entry
    for (int index = 0; index < len; index++) {
        hashOrigin = (P * hashOrigin + origin[index]) % Q;
        hashShifted = (P * hashShifted + shifted[index]) % Q;
    }

    // Calculate first multiplier (mod power)
    int maxP = 1;

    for (int index = 0; index < len - 1; index++) {
        maxP = (maxP * P) % Q;
    }

    // Iterate possible shiftings
    for (int shift = 0; shift < len; shift++) {
        if (hashShifted == hashOrigin) {
            std::cout << shift << std::endl;
            bool found = true;

            for (int index = 0; index < len; index++) {
                if (shifted[(index + shift) % len] != origin[index]) {
                    found = false;
                    break;
                }
            }

            if (found) {
                return shift;
            }
        }

        hashShifted = (P * (hashShifted - maxP * shifted[shift]) + shifted[shift]) % Q;

        // If hash is negative
        if (hashShifted < 0) {
            hashShifted += Q;
        }
    }

    // If none of entries are matching
    return -1;
}
