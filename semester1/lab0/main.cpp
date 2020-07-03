#include <iostream>
using namespace std;



int main()
{
    int a, b, n;
    int c[10];

    cout << "Введіть проміжок: ";
    cin >> a >> b;

    for (int i = a; i <= b; i++)
    {
        int j = abs(i);
        for (int x = 0; x <= 9; x++)
        {
            c[x] = 0;
        }

        while (j >= 10)
        {
            n = j % 10;
            j /= 10;

            if (c[n])
            {
                j = -10;
                break;
            }
            else c[n] += 1;
        }
        if (j != -10 && not c[j])
        {
            cout << i << endl;
        }
    }
    return 0;
}