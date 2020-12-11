#include "string"


int isShifted(const std::string &origin,
              const std::string &shifted) {
    // Check if string are equal

    if (origin == shifted) {
        return 0;
    }

    // Init values

    const int n = origin.length();  // Save length of string

    int s = 0;  // Sum of all chars
    int si = 0;  // Sum of shifted chars

    for (char symbol: origin) {
        s += symbol;
    }

    // Calculate subtraction of origin and shifted

    int sub = 0;

    for (int i = 0; i < n; i++) {
        sub += (i + 1) * (shifted[i] - origin[i]);
    }

    // Iterate through possible shift values

    int value;

    for (int d = 1; d < n; d++) {
        si += origin[n - d]; // Add shifted char
        value = d * s - n * si; // Calculate value for current shift

        if (value == sub) {
            return d;  // If value == sub then shift found
        }
    }

    return -1;  // If shift not found
}
