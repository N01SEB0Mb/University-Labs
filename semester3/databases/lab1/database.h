#ifndef DATABASE_DB_H
#define DATABASE_DB_H

#include <stdio.h>
#include <stdlib.h>

// Database fields sizes
#define INFO_SIZE (64)
#define MESSAGE_SIZE (512)

// Database files path
#define MESSAGES_PATH ("/home/noisebomb/PycharmProjects/University-Labs/semester3/databases/database/messages.db")
#define MESSAGES_TMP_PATH ("/home/noisebomb/PycharmProjects/University-Labs/semester3/databases/database/messages.tdb")
#define USERS_PATH ("/home/noisebomb/PycharmProjects/University-Labs/semester3/databases/database/users.db")
#define USERS_TMP_PATH ("/home/noisebomb/PycharmProjects/University-Labs/semester3/databases/database/users.tdb")

// Status codes
#define SUCCESS (0);
#define NO_FILE (1);
#define NOT_FOUND (2);


// User structure
struct User {
    long ID;
    char username[INFO_SIZE];
    char password[INFO_SIZE];
    long long number;
};

// Message structure
struct Message {
    long fromID;
    char text[MESSAGE_SIZE];
};


int getMaster();

int getSlave();

int deleteMaster();

int deleteSlave();

int updateMaster();

int updateSlave();

int insertMaster();

int insertSlave();

int utilityMaster();

int utilitySlave();

int countMaster();

int countSlave();

int deleteMasterByID(int ID);

int deleteSlaveByNumber(int number);

int deleteSlaveByID(int ID);

int updateMasterByID(int ID);

int updateSlaveByNumber(int number);

void utilityMasterFromStruct(struct User *user);

void utilitySlaveFromStruct(struct Message *message);

int utilityMasterSmall();

int utilitySlaveSmall();

void help();


#endif
