#include "MQTTmessage.h"

MQTTmessage::MQTTmessage(const mosquitto_message *pMessage,
                         messageType mesgType)
   : pMessage_{pMessage}
   , topic_{pMessage->topic}
   , payload_{""}
   , pPayloadBinary_{nullptr}
   , payloadLength_{pMessage->payloadlen}
{
   switch (mesgType) {
      case messageType::STRING:
         payload_ = std::string{static_cast<char *>(pMessage_->payload)};
         break;
      case messageType::BINARY:
         pPayloadBinary_ = static_cast<u_int8_t *>(pMessage_->payload);
         break;
   }
}
