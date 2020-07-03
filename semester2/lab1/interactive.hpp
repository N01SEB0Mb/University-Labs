#include <iostream>
#include <string>

using namespace std;

void message(int operation) {
  switch (operation) {
    case 0: // Add
      cout << "Message add" << endl;
      break;
    case 1: // Get
      cout << "Message get" << endl;
      break;
    case 2: // Get all
      cout << "Message all" << endl;
      break;
    case 3: // Edit
      cout << "Message edit" << endl;
      break;
    case 4: // Delete
      cout << "Message delete" << endl;
      break;
    case 5: // Search
      cout << "Message search" << endl;
      break;
  }
}

void server(int operation) {
  switch (operation) {
    case 0: // Select
      cout << "Server select" << endl;
      break;
    case 1: // Create
      cout << "Server create" << endl;
      break;
    case 2: // Create random
      cout << "Server create random" << endl;
      break;
    case 3: // Delete
      cout << "Server delete" << endl;
      break;
  }
}

void text(int operation) {
  switch (operation) {
    case 0: // Save
      cout << "Text save" << endl;
      break;
    case 1: // Load
      cout << "Text load" << endl;
      break;
  }
}

void binary(int operation) {
  switch (operation) {
    case 0: // Save
      cout << "Binary save" << endl;
      break;
    case 1: // Load
      cout << "Binary load" << endl;
      break;
  }
}

void demonstration() {}

void help() {
  cout << "Message management:" << endl;

  cout << " -ma: Add message to current server" << endl;
  cout << " -mg: Get message from current server" << endl;
  cout << " -mw: Get all messages from current server" << endl;
  cout << " -me: Edit message from current server" << endl;
  cout << " -md: Delete message from current server" << endl;
  cout << " -ms: Search message on current server" << endl << endl;

  cout << "Server management:" << endl;

  cout << " -ss: Select server" << endl;
  cout << " -sc: Create server" << endl;
  cout << " -sr: Create server with random info" << endl;
  cout << " -sd: Delete server" << endl << endl;

  cout << "Server database management:" << endl;

  cout << " -ts: Save server database to text file" << endl;
  cout << " -tl: Load server database from text file" << endl;

  cout << " -bs: Save server database to binary file" << endl;
  cout << " -bl: Load server database from binary file" << endl << endl;

  cout << "Other:" << endl;

  cout << " -h:  List of commands (This menu)" << endl;
  cout << " -dm: Demonstration mode" << endl;
  cout << " -ex: Exit" << endl;
}

void interactive() {
  string cmd;

  cout << "This is interactive mode" << endl;
  cout << "Type \"-h\" to get list of commands" << endl;

  while (true) {
    cin >> cmd;

    if (cmd == "-h") {
      help();
    }
    else if (cmd == "-ma") {
      message(0);
    }
    else if (cmd == "-mg") {
      message(1);
    }
    else if (cmd == "-mw") {
      message(2);
    }
    else if (cmd == "-me") {
      message(3);
    }
    else if (cmd == "-md") {
      message(4);
    }
    else if (cmd == "-ms") {
      message(5);
    }
    else if (cmd == "-ss") {
      server(0);
    }
    else if (cmd == "-sc") {
      server(1);
    }
    else if (cmd == "-sr") {
      server(2);
    }
    else if (cmd == "-sd") {
      server(3);
    }
    else if (cmd == "-ts") {
      text(0);
    }
    else if (cmd == "-tl") {
      text(1);
    }
    else if (cmd == "-bs") {
      binary(0);
    }
    else if (cmd == "-bl") {
      binary(1);
    }
    else if (cmd == "-dm") {
      demonstration();
    }
    else if (cmd == "-ex") {
      exit(0);
    }
    else {
      cout << "Unknown command. Type \"-h\" to get list of commands" << endl;
    }
  }
}