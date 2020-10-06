#include "CommandProcessor.h"
#include "MQTTconfig.h"
#include "Tokenizer.h"
#include "Topic.h"

#include <iostream>

#define CERR std::cerr << className_ << "::" << __func__ << "()\n   "

CommandProcessor::CommandProcessor(const std::string &appname,
                                   const std::string &clientname,
                                   const std::string &host, int port)
   : mosqpp::mosquittopp{(HOSTNAME + appname + clientname).c_str()}
   , className_{__func__}
   , appname_{appname}
   , clientname_{clientname}
   , topicRoot_{MQTT_TOPIC_ROOT}
   , topicCommandRoot_{MQTT_TOPIC_ROOT}
   , commands_{}
{
   topicRoot_.add(appname_).add(clientname_);
   topicCommandRoot_.add(appname_).add(clientname_).add("command");
   CERR << "command topic = " << topicCommandRoot_.c_str() << std::endl;
   connect(host.c_str(), port, MQTT_KEEP_ALIVE);
}

CommandProcessor::~CommandProcessor()
{
   disconnect();
}

void CommandProcessor::on_message(const mosquitto_message *message)
{
   executeCommand(static_cast<char *>(message->payload));
}

void CommandProcessor::on_connect(int rc)
{
   CERR << "connected with rc = " << rc << std::endl;
   if (rc == 0) {
      /// Only attempt to subscribe on a successful connect.
      auto rc1 = subscribe(nullptr, topicCommandRoot_.c_str());
      if (rc1 != MOSQ_ERR_SUCCESS) {
         std::cerr << "   MQTT subscribe error" << std::endl;
      }
   }
}

void CommandProcessor::on_log(int level, const char *str)
{
   // CERR << "level = " << level << "\n   " << str << std::endl;
}

void CommandProcessor::registerCommand(const std::string &command,
                                       commandfunction cfunction)
{
   CERR << "command = " << command << std::endl;
   if (!commandIsRegistered(command)) {
      commands_[command] = cfunction;
      publishInfo(command, " registered");
   } else {
      publishWarning(command, " already registered");
   }
}

void CommandProcessor::executeCommand(const std::string &command)
{
   std::vector<std::string> commandpars{split(command)};
   CERR << "command = " << command << std::endl;
   if (commandIsRegistered(commandpars[0])) {
      commands_[commandpars[0]](std::vector<std::string>(
         std::begin(commandpars) + 1, std::end(commandpars)));
   } else {
      publishError(commandpars[0], " unknown command");
   }
}

void CommandProcessor::executeCommands(const std::vector<std::string> &commands)
{
   for (const auto &command : commands) {
      executeCommand(command);
   }
}

bool CommandProcessor::commandIsRegistered(const std::string &command) const
{
   return commands_.find(command) != std::end(commands_);
}

void CommandProcessor::publishAddition(const std::string &topicAddition,
                                       const std::string &message)
{
   Topic topic{topicRoot_};
   topic.add(topicAddition);
   publish(nullptr, topic.c_str(), message.size(), message.c_str());
}

void CommandProcessor::publishReturn(const std::string &command,
                                     const std::string &message)
{
   publishAddition("command/" + command + "/return", message);
}

void CommandProcessor::publishInfo(const std::string &command,
                                   const std::string &message)
{
   publishAddition("command/" + command + "/info", message);
}

void CommandProcessor::publishWarning(const std::string &command,
                                      const std::string &message)
{
   publishAddition("command/" + command + "/warning", message);
}

void CommandProcessor::publishError(const std::string &command,
                                    const std::string &message)
{
   publishAddition("command/" + command + "/error", message);
}
