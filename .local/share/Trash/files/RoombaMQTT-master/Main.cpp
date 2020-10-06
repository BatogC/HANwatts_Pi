/**
 *@author Pham Minh Nhat
 *@author Bas de Quinze 
 */

#include "AppInfo.h"
#include "RoombaMQTT.h"

#define LOOPTIME 5

int main() {
    std::cout << APPNAME_VERSION << std::endl;

    mosqpp::lib_init();

    RoombaMQTT client(APPNAME, "RoombaHAN",
                      "broker.hivemq.com", 1883,
                      LOOPTIME);
    
    while(1) {
        int rc{client.loop()};
        if (rc) {
            std::cerr << "Reconecting..." << std::endl;
            client.reconnect();
        }
    }

    mosqpp::lib_cleanup();

    return 0;   
}