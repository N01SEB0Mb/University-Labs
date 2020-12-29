#ifndef DATABASE_DB_H
#define DATABASE_DB_H

#include <stdio.h>
#include <stdlib.h>

// Database fields sizes
#define INFO_SIZE (64)
#define MESSAGE_SIZE (512)

// Database files path
#define MESSAGES_PATH ("../database/messages.db")
#define MESSAGES_TMP_PATH ("../database/messages.tdb")
#define USERS_PATH ("../database/users.db")
#define USERS_TMP_PATH ("../database/users.tdb")

// Status codes
#define SUCCESS (0)
#define NO_FILE (1)
#define NOT_FOUND (2)

#define SEP_LEN (24)


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


void separator(char sep);

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

int deleteMasterByID(long ID);

int deleteSlaveByNumber(int number);

int deleteSlaveByID(long ID);

int updateMasterByID(long ID);

int updateSlaveByNumber(int number);

void utilityMasterFromStruct(struct User *user);

void utilitySlaveFromStruct(struct Message *message);

int utilityMasterSmall();

void help();


#endif
