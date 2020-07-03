#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

int main()
{
  int n;
  bool pos1 = true;
  bool pos2 = true;

  cin >> n;

  if (!n)
  {
    cout << -1;
    return 0;
  }

  vector<pair<int, int>> a;
  a.resize(n);

  for (int i = 0; i < 2 * n; i++)
  {
    if (i < n)
      cin >> a[i].first;
    else
      cin >> a[i - n].second;
  }

  sort(a.begin(), a.end());

  for (int i = 1; i < n; i++)
  {
    if (a[i - 1].second > a[i].second)
    {
      pos1 = false;
      break;
    }
  }

  if (pos1)
  {
    for (int i = 0; i < 2 * n; i++)
    {
      if (i == n)
        cout << endl;
      if (i < n)
        cout << a[i].first << " ";
      else
        cout << a[i - n].second << " ";
    }
    return 0;
  }

  for (auto i: a)
  {
    swap(i.first, i.second);
  }

  sort(a.begin(), a.end());

  for (int i = 1; i < n; i++)
  {
    if (a[i - 1].second > a[i].second)
    {
      pos2 = false;
      break;
    }
  }

  if (pos2)
  {
    for (int i = 0; i < 2 * n; i++)
    {
      if (i == n)
        cout << endl;
      if (i < n)
        cout << a[i].second << " ";
      else
        cout << a[i - n].first << " ";
    }
    return 0;
  }

  cout << -1;
  return 0;
}