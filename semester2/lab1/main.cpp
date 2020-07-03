#include <iostream>
#include <string>
#include "interactive.hpp"

using namespace std;

struct Time {
  uint8_t Hour;
  uint8_t Minute;
  uint8_t Second;
};

struct Date {
  uint8_t Day;
  uint8_t Month;
  uint16_t Year;
};

struct ServerInfo {
  string name;
  string url;
  Date originDate;
  Time originTime;
  int maxUsers;
  uint8_t type;
  /*
   0: News;
   1: Question;
   2: Answer;
   3: Invite;
   4: Comment;
  */
  float spamProbability;
};

struct MessageInfo {
  string text;
  string type;
  string date;
  string time;
  string from;
  string to;
};

int main()
{
  interactive();

  return 0;
}
