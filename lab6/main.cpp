#include <iostream>
#include <fstream>
#include <string>

using namespace std;

ifstream input("input.txt");
ofstream output("output.txt");
string reader;

int min_len;

bool is_palyndrom(string a)
{
  for (int i = 0; i < a.size() / 2; i++)
  {
    if (a[i] != a[a.size() - 1 - i])
    {
      return false;
    }
  }
  return true;
}

string change(string a)
{
  string response, temp_word;

  for (auto i: a + " ")
  {
    if (i == ' ')
    {
      bool is_pal = false;
      string temp_s;

      for (int size = min_len; size <= temp_word.size(); size++)
      {
        for (int j = 0; j <= temp_word.size() - size && !is_pal; j++)
        {
          temp_s = "";
          for (int x = 0; x < size; x++)
          {
            temp_s += temp_word[x + j];
          }
          if (is_palyndrom(temp_s))
          {
            is_pal = true;
            break;
          }
        }
      }

      if (!is_pal)
      {
        response += temp_word;
      }

      temp_word.clear();
      response += i;
    }
    else
    {
      temp_word += i;
    }
  }

  return response;
}

int main()
{
  cin >> min_len;

  while (!input.eof())
  {
    getline(input, reader);
    output << change(reader) << endl;
  }
}
