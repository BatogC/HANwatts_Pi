#ifndef PARLOOP_H
#define PARLOOP_H

#include "ChronoUtils.h"

#include <atomic>
#include <chrono>
#include <condition_variable>
#include <functional>
#include <iostream>
#include <mutex>
#include <thread>

// namespace chnl = std::chrono_literals;
using callbackFunction_t = std::function<void()>;

/// Utility class for provinding a loop executing a callback function #cbf
/// in a thread. After executing this function this thread will sleep for
/// #loopTimeSeconds seconds. This class in non-copyable.
/// RAII: the thread is created by the constructor and is stopped in the
/// destructor #~Parloop.
template <typename Duration = std::chrono::seconds>
class ParLoop
{
public:
   ParLoop(callbackFunction_t cbf, int loopDuration)
      : loopDuration_{loopDuration}
      , isRunning_{true}
      , cbf_{cbf}
      , threadLooping_{&ParLoop::loop, this}
      , cv_{}
      , mtx_{}
   {
      static_assert(is_chrono_duration_v<Duration>,
                    "Template parameter is not an std::chrono::duration type!");
   }
   ParLoop(const ParLoop &other) = delete;
   ParLoop &operator=(const ParLoop &other) = delete;
   ~ParLoop() { stop(); }

private:
   Duration loopDuration_;
   std::atomic<bool> isRunning_;
   callbackFunction_t cbf_;
   std::thread threadLooping_;
   std::condition_variable cv_;
   std::mutex mtx_;

   void loop()
   {
      while (isRunning_) {
         cbf_();
         std::unique_lock<std::mutex> lock{mtx_};
         if (cv_.wait_for(lock, loopDuration_,
                          [this]() { return not isRunning_; })) {
            break;
         }
      }
   }

   void stop()
   {
      isRunning_ = false;
      cv_.notify_all();
      if (threadLooping_.joinable()) {
         threadLooping_.join();
      }
   }
};

#endif
