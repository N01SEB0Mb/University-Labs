#include <iostream>
#include <cmath>

using namespace std;


// Числа Кармайкла

int main()
{
  int n;
  cin >> n;
  int n_ = n;

  int m[n];
  for (int i = 0; i < n; i++)
    m[i] = 0;

  for (int i = 2; i <= sqrt(n); i++)
  {
    for (int j = 2; j <= n / i; j++)
    {
      m[i * j - 1] = 1;
    }
  }

  bool b = m[n - 1];

  if (b)
  {
    for (int i = 2; i <= sqrt(n); i++)
    {
      if (!(n % (i * i)))
      {
        b = false;
        break;
      }
    }
  }

  if (b)
  {
    while (n_ != 1)
    {
      int i = 2;
      while (n_ % i)
      {
        i++;
      }
      n_ /= i;
      if (((n - 1) % (i - 1)))
      {
        b = false;
        break;
      }
    }
  }

  cout << b;

  return 0;
}