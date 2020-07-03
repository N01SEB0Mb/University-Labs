#include <iostream>
#include <bitset>
#include <string>

using namespace std;

const int init_bits = 64;

bitset<init_bits> bit2gray(const bitset<init_bits> n)
{
  return (n ^ (n >> 1));
}

bitset<init_bits> gray2bin(const bitset<init_bits> n)
{
  int i = 1;
  bitset<init_bits> answer = n, j;

  while (1)
  {
    j = (answer >> i);
    answer ^= j;
    if (j.to_ulong() <= 1 || j == 16)
      return answer;
    i <<= 1;
  }
}

int main ()
{
  string input;
  cin >> input;

  bitset<init_bits> ans1 = bit2gray(bitset<init_bits>(input));
  bitset<init_bits> ans2 = gray2bin(bitset<init_bits>(input));

  cout << "Binary code -> Gray code" << endl;

  for (int i = input.length(); i; i--)
  {
    cout << ans1[i - 1];
  }

  cout << endl << "Gray code -> Binary code" << endl;

  for (int i = input.length(); i; i--)
  {
    cout << ans2[i - 1];
  }
}