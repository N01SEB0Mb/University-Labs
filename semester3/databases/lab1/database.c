#include <stdio.h>

#include "database.h"


void separator(char sep) {
    // Print separator SEP_LEN times
    for (int _ = 0; _ < SEP_LEN; _++) {
        printf("%c", sep);
    }
    // Next line
    printf("\n");
}


int getMaster() {
    // Init file and data variables
    FILE *fp;
    struct User user;
    long ID;

    // Try opening file
    if ((fp = fopen(USERS_PATH, "rb")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Get ID
    utilityMasterSmall();
    printf("Type user ID: ");
    scanf("%ld", &ID);

    // Search ID
    while (fread(&user, sizeof(struct User), 1, fp) == 1) {
        if (user.ID == ID) {
            break;
        }
    }

    // If ID not found
    if (user.ID != ID) {
        perror("User with this ID not found");
        fclose(fp);
        return NOT_FOUND;
    }

    // Print info
    utilityMasterFromStruct(&user);

    // Close file
    fclose(fp);

    // Return success code
    return SUCCESS;
}


int getSlave() {
    // Init file and data variables
    FILE *fp;
    struct Message message;
    long ID;

    // Try opening file
    if ((fp = fopen(MESSAGES_PATH, "rb")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Get ID
    utilitySlave();
    printf("Type message ID: ");
    scanf("%ld", &ID);

    // Search ID
    while (fread(&message, sizeof(struct Message), 1, fp) == 1) {
        if (message.fromID == ID) {
            // Print info
            utilitySlaveFromStruct(&message);
            break;
        }
    }

    // If ID not found
    if (message.fromID != ID)
        perror("Message with this ID not found");

    // Close file
    fclose(fp);

    // Return success status
    return SUCCESS;
}


int deleteMaster() {
    // ID variable
    long ID;

    // Get ID
    utilityMasterSmall();
    printf("Type user ID: ");
    scanf("%ld", &ID);

    separator('=');

    // Deleting master
    deleteMasterByID(ID);

    // Return success status
    return SUCCESS;
}


int deleteSlave() {
    int number;

    // Request number
    utilitySlave();
    printf("Type message number: ");
    scanf("%d", &number);

    separator('=');

    // Delete slave
    deleteSlaveByNumber(number);

    // Return success status
    return SUCCESS;
}


int updateMaster() {
    // Id variable
    long ID;

    // Request ID of master
    utilityMasterSmall();
    printf("Type user ID: ");
    scanf("%ld", &ID);

    // Return master updating status
    return updateMasterByID(ID);
}


int updateSlave() {
    // Slave number variable
    int number;

    // Request number of slave
    utilitySlave();
    printf("Type message number: ");
    scanf("%d", &number);

    // Return slave updating status
    return updateSlaveByNumber(number);
};


int insertMaster() {
    // Init file and data variables
    FILE *fp;
    struct User user;
    long ID;

    // Try opening file
    if ((fp = fopen(USERS_PATH, "a+b")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Get user ID
    separator('=');
    printf("Type user ID: ");
    scanf("%ld", &ID);
    separator('-');

    // Search ID
    while (fread(&user, sizeof(struct User), 1, fp) == 1) {
        if (ID == user.ID) {
            perror("User with such ID already exists.");
            return NOT_FOUND;
        }
    }

    // Select ID
    user.ID = ID;

    // Get info
    printf("Type user info\n");
    separator('-');

    printf("Username: ");
    scanf("%s", user.username);

    printf("Password: ");
    scanf("%s", user.password);

    printf("Phone number: ");
    scanf("%lld", &user.number);

    separator('-');

    // Write and close file
    fwrite(&user, sizeof(struct User), 1, fp);
    fclose(fp);

    // Return successful result
    return SUCCESS;
}


int insertSlave() {
    // Init file and data variables
    FILE *fp;
    struct Message message;

    // Try opening file
    if ((fp = fopen(MESSAGES_PATH, "ab")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Get user ID
    separator('=');
    printf("Type user ID: ");
    scanf("%ld", &message.fromID);
    separator('-');
    printf("Text: ");
    scanf("%s", message.text);
    separator('=');

    // Write and close file
    fwrite(&message, sizeof(struct Message), 1, fp);
    fclose(fp);

    // Return success status
    return SUCCESS;
}


int utilityMaster() {
    // Init file and data variables
    FILE *file;
    struct User user;

    // Try opening file
    if ((file = fopen(USERS_PATH, "rb")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Print users
    printf("USERS\n");

    while (fread(&user, sizeof(struct User), 1, file) == 1) {
        // Print info
        separator('-');
        printf("ID          : %ld\n"
               "Username    : %s\n"
               "Password    : %s\n"
               "Phone number: %lld\n",
               user.ID, user.username, user.password, user.number);
    }

    separator('=');

    // Close file
    fclose(file);

    // Return success status
    return SUCCESS;
}


int utilitySlave() {
    // Init file and data variables
    FILE *file;
    struct Message message;

    // Try opening file
    if ((file = fopen(MESSAGES_PATH, "rb")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Index init
    int index = 0;

    // Print info
    separator('=');
    printf("MESSAGES\n");
    separator('-');

    while (fread(&message, sizeof(struct Message), 1, file) == 1) {
        printf("[%d] %ld: %s\n",
               index, message.fromID, message.text);
        index++;
    }

    separator('=');

    // Close file
    fclose(file);

    // Return success status
    return SUCCESS;
}


int countMaster() {
    // Init file and data variables
    FILE *fp;
    struct User user;

    int count = 0;

    // Try opening file
    if ((fp = fopen(USERS_PATH, "rb")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Count users
    while (fread(&user, sizeof(struct User), 1, fp) == 1) {
        count++;
    }

    // Print count
    separator('-');
    printf("Total users: %d\n", count);
    separator('=');

    // Close file
    fclose(fp);

    // Return success status
    return SUCCESS;
}


int countSlave() {
    // Init file and data variables
    FILE *fp;
    struct Message message;
    long ID;

    int count = 0;

    // Try opening file
    if ((fp = fopen(MESSAGES_PATH, "rb")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Get ID of master
    utilityMasterSmall();
    printf("Type user ID or -1 (all): \n");
    scanf("%ld", &ID);
    separator('-');

    // Count
    while (fread(&message, sizeof(struct Message), 1, fp) == 1) {
        if (ID == -1 || message.fromID == ID) {
            count++;
        } else {
            count++;
            break;
        }
    }

    // Print info
    printf("Total messages: %d\n", count);
    separator('=');

    // Close file
    fclose(fp);

    // Return success status
    return SUCCESS;
}


int deleteMasterByID(long ID) {
    // Init file and data variables
    FILE *getFile;
    FILE *putFile;
    struct User user;

    int found = 0;

    // Try opening files
    if ((getFile = fopen(USERS_PATH, "rb")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    if ((putFile = fopen(USERS_TMP_PATH, "ab")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Write all not equal to ID
    while (fread(&user, sizeof(struct User), 1, getFile) == 1) {
        if (user.ID != ID) {
            fwrite(&user, sizeof(struct User), 1, putFile);
        }
        else {
            found = 1;
        }
    }

    // Close files
    fclose(getFile);
    fclose(putFile);

    // If ID was found
    if (found) {
        // Delete slaves
        deleteSlaveByID(ID);

        // Swap files
        remove(USERS_PATH);
        return rename(USERS_TMP_PATH, USERS_PATH);
    } else {
        // Remove temp file
        remove(USERS_TMP_PATH);
        perror("User with such ID not found");
        return NOT_FOUND;
    }
}


int deleteSlaveByNumber(int number) {
    // Init file and data variables
    FILE *getFile;
    FILE *putFile;
    struct Message message;

    int found = 0;

    // Try opening files
    if ((getFile = fopen(MESSAGES_PATH, "rb")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    if ((putFile = fopen(MESSAGES_TMP_PATH, "ab")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Index variable init
    int index = 1;


    // Write all except number
    while (fread(&message, sizeof(struct Message), 1, getFile) == 1) {
        if (index != number) {
            fwrite(&message, sizeof(struct Message), 1, putFile);
        }
        else {
            found = 1;
        }

        index++;
    }

    // Close files
    fclose(getFile);
    fclose(putFile);

    // If ID was found
    if (found) {
        // Swap files
        remove(MESSAGES_PATH);
        return rename(MESSAGES_TMP_PATH, MESSAGES_PATH);
    } else {
        // Remove temp file
        remove(MESSAGES_TMP_PATH);
        perror("Message with this number not found");

        return NOT_FOUND;
    }
}


int deleteSlaveByID(long ID) {
    // Init file and data variables
    FILE *getFile;
    FILE *putFile;
    struct Message message;

    // Try opening files
    if ((getFile = fopen(MESSAGES_PATH, "rb")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;

    }
    if ((putFile = fopen(MESSAGES_TMP_PATH, "ab")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Write all except ID
    while (fread(&message, sizeof(struct Message), 1, getFile) == 1) {
        if (message.fromID != ID) {
            fwrite(&message, sizeof(struct Message), 1, putFile);
        }
    }

    // Close files
    fclose(getFile);
    fclose(putFile);

    // Swap files
    remove(MESSAGES_PATH);
    return rename(MESSAGES_TMP_PATH, MESSAGES_PATH);
}


int updateMasterByID(long ID) {
    // Init file and data variables
    FILE *fp;
    struct User user;

    int found = 0;

    // Try opening file
    if ((fp = fopen(USERS_PATH, "rb+")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Read until found
    while (fread(&user, sizeof(struct User), 1, fp) == 1) {
        if (user.ID == ID) {
            found = 1;
            break;
        }
    }

    // If not found
    if (!found) {
        perror("User with such ID not found");
        return NOT_FOUND;
    }

    // Print user info
    utilityMasterFromStruct(&user);

    // Get info
    printf("Type new user info\n");
    separator('-');

    printf("Username: ");
    scanf("%s", user.username);

    printf("Password: ");
    scanf("%s", user.password);

    printf("Phone number: ");
    scanf("%lld", &user.number);

    separator('-');

    // Update info
    fseek(fp, -sizeof(struct User), SEEK_CUR);
    fwrite(&user, sizeof(struct User), 1, fp);

    // Print success
    printf("Successfuly updated.\n");
    separator('=');

    // Close file
    fclose(fp);

    // Return success status
    return SUCCESS;
}


int updateSlaveByNumber(int number) {
    // Init file and data variables
    FILE *fp;
    struct Message message;

    int index = 0;
    int found = 0;

    // Try opening file
    if ((fp = fopen(MESSAGES_PATH, "r+b")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Iterate until number found
    while (fread(&message, sizeof(struct Message), 1, fp) == 1 && !found) {
        index++;

        if (index == number) {
            found = 1;
        }
    }

    // If not found
    if (!found) {
        perror("Message with this number not found");
        return NOT_FOUND;
    }

    // Print user info
    utilitySlaveFromStruct(&message);

    // Get info
    printf("Type new text: \n");
    scanf("%s", message.text);

    // Update info
    fseek(fp, -sizeof(struct Message), SEEK_CUR);
    fwrite(&message, sizeof(struct Message), 1, fp);

    // Close file
    fclose(fp);

    // Return success status
    return SUCCESS;
}


void utilityMasterFromStruct(struct User *user) {
    // Print info
    separator('=');
    printf("USER:\n");
    separator('-');
    printf("Username    : %s\n"
           "Password    : %s\n"
           "Phone number: %lld\n",
           user->username, user->password, user->number);
    separator('=');
}


void utilitySlaveFromStruct(struct Message *message) {
    // Print info
    separator('=');
    printf("MESSAGE:\n");
    separator('-');
    printf("Text: %s\n", message->text);
    separator('=');
}


int utilityMasterSmall() {
    // Init file and data variables
    FILE *file;
    struct User user;

    // Try opening file
    if ((file = fopen(USERS_PATH, "rb")) == NULL) {
        perror("Error occured while opening file");
        return NO_FILE;
    }

    // Print info
    separator('=');
    printf("USERS\n");
    separator('-');

    while (fread(&user, sizeof(struct User), 1, file) == 1) {
        printf("%ld: %s\n", user.ID, user.username);
    }

    separator('=');

    // Close file
    fclose(file);

    // Return success status
    return SUCCESS;
}
