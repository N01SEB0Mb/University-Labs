#include "database.h"


void scenario() {
    // Start
    printf("%s","Operations script:\n");

    // Insert 5 masters
    printf("%s","Insert master 5 times\n");
    for (int _ = 0; _ < 5; _++) {
        insertMaster();
    }

    // Insert 6 slaves
    printf("%s","Insert 1 slave to 1-st master, 2 slaves to 2-nd and 3 slaves to 3-rd\n");
    for(int _ = 0; _ < 6; _++) {
        insertSlave();
    }

    // Output
    printf("%s", "Output:\n");
    utilityMaster();
    utilitySlave();

    // Delete master
    printf("%s","Delete 2-nd master\n");
    deleteMaster();

    // Delete slave
    printf("%s", "Delete slave from 3-rd master\n");
    deleteSlave();

    // Output
    printf("%s", "Output:\n");
    utilityMaster();
    utilitySlave();

    // Instert master and slave
    printf("%s", "Now we will insert one more master and slave for it.\n");
    insertMaster();
    insertSlave();

    // Update master and slave
    printf("%s","Update 1-st master and his slave.\n");
    updateMaster();
    updateSlave();

    // Output
    printf("%s", "Output:\n");
    utilityMaster();
    utilitySlave();

    // End
    printf("%s","End of script...\n");
}


void help(){
    printf("Choose operation using format: <tp>, where t is master(0) or slave(1) and p is operation:\n"
           "1 - Get\n"
           "2 - Delete\n"
           "3 - Update\n"
           "4 - Insert\n"
           "5 - Count\n"
           "6 - Utility\n"
           "0 - Exit\n"
           "Example: 01 - Get master, 13 - Update slave\n");
}


void interactive() {
    int action;

    while (1) {
        // Output help message
        help();

        // Read operation
        printf("Type operation: ");
        scanf("%d", &action);

        // Choose operation
        switch (action) {
            case 1:
                getMaster();
                break;
            case 11:
                getSlave();
                break;
            case 2:
                deleteMaster();
                break;
            case 12:
                deleteSlave();
                break;
            case 3:
                updateMaster();
                break;
            case 13:
                updateSlave();
            case 4:
                insertMaster();
                break;
            case 14:
                insertSlave();
                break;
            case 5:
                countMaster();
                break;
            case 15:
                countSlave();
                break;
            case 6:
                utilityMaster();
                break;
            case 16:
                utilitySlave();
                break;
            case 0:
                exit(0);
            default:
                perror("Unknown operation\n");
                break;
        }
    }
}


int main() {
    int mode;

    printf("Choose mode, interactive (0) or scenario (1): ");
    scanf("%d", &mode);

    switch (mode) {
        case 0:
            interactive();
            break;
        case 1:
            scenario();
            break;
        default:
            perror("Unknown mode given");
            return -1;
    }

    return 0;
}