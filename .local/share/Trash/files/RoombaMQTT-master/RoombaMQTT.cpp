#include "RoombaMQTT.h"
#include <nlohmann/json.hpp>
#include "AppInfo.h"

using json = nlohmann::json;

RoombaMQTT::RoombaMQTT(const std::string &appname, const std::string &clientname,
                       const std::string &host, int port, int loopTime)
    : CommandProcessor(appname, clientname, host, port),
      loop_{std::bind(&RoombaMQTT::StatusUpdate, this), loopTime} {
    using namespace std::placeholders;
    registerCommand("HiMosquitto", std::bind(&RoombaMQTT::HiMosquitto, this, _1));
}

RoombaMQTT::~RoombaMQTT() {}

void RoombaMQTT::StatusUpdate() {
    json Status_ = {
        {"AppName", APPNAME},
        {"Version", VERSION},
        {"Function", {
            "Heartbeat notify message",
            "Receive message from MQTT broker"
        }}
    };
    std::cout << Status_ << std::endl;
}

void RoombaMQTT::HiMosquitto(const std::vector<std::string> &commmandParameters) {
    std::cout << "Received from MQTT broker" << commmandParameters[0] << std::endl;
    std::cout << "Hi Mosquitto" << std::endl;
}