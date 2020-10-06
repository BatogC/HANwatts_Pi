#ifndef ROOMBAMQTT_H
#define ROOMBAMQTT_H

#include "CommandProcessor.h"
#include "ParLoop.h"

class RoombaMQTT: public CommandProcessor {
    public:
        RoombaMQTT(const std::string &appname, const std::string &clientname,
                   const std::string &host, int port, int loopTime);
        ~RoombaMQTT();
    private:
        void StatusUpdate();
        void HiMosquitto(const std::vector<std::string> &commmandParameters);
        ParLoop <std::chrono::seconds> loop_;
};

#endif