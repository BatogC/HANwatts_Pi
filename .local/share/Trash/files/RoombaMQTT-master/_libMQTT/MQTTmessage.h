#ifndef MQTTMESSAGE_H
#define MQTTMESSAGE_H

#include "mosquittopp.h"

#include <string>

class MQTTmessage
{
public:
   enum class messageType { STRING, BINARY };

   explicit MQTTmessage(const mosquitto_message *pMessage,
                        messageType mesgType = messageType::STRING);
   MQTTmessage(const MQTTmessage &other) = delete;
   MQTTmessage &operator=(const MQTTmessage &) = delete;
   ~MQTTmessage() = default;

   std::string getTopic() const { return topic_; }
   std::string getPayload() const { return payload_; }
   uint8_t *getPayloadBinary() const { return pPayloadBinary_; }
   int getPayloadBinaryLength() const { return payloadLength_; }

private:
   const mosquitto_message *pMessage_;
   const std::string topic_;
   std::string payload_;
   uint8_t *pPayloadBinary_;
   int payloadLength_;
};

#endif
