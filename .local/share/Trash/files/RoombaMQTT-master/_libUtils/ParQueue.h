#ifndef PARQUEUE_H
#define PARQUEUE_H

#include <atomic>
#include <condition_variable>
#include <functional>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>

/// The template class ParQueue represents a queue.
/// Provided data will be pushed into the queue.
/// Can be applied for consuming data in a thread safe way in a callback
/// function #handleData.
template <typename D> class ParQueue
{
public:
   ParQueue(std::function<void(const D &)> handleData)
      : handleData_{handleData}
      , queueMutex_{}
      , queueConditionVar_{}
      , queue_{}
      , running_{true}
      , threadConsuming_{&ParQueue::consume, this}
   {
   }
   ParQueue(const ParQueue &other) = delete;
   ParQueue &operator=(const ParQueue &other) = delete;
   ~ParQueue() { stop(); }

   void provide(const D &data)
   {
      {
         std::lock_guard<std::mutex> lg(queueMutex_);
         queue_.push(data);
      } // Release lock
      queueConditionVar_.notify_one();
   }

private:
   std::function<void(const D &)> handleData_;
   std::mutex queueMutex_;
   std::condition_variable queueConditionVar_;
   std::queue<D> queue_;
   std::atomic<bool> running_;
   std::thread threadConsuming_;

   void consume()
   {
      while (running_) {
         D data;
         {
            std::unique_lock<std::mutex> ul(queueMutex_);
            queueConditionVar_.wait(
               ul, [this] { return (not queue_.empty()) or (not running_); });
            if (running_) {
               data = queue_.front();
               queue_.pop();
            }
         } // Scope based release lock
         if (running_) {
            handleData_(data);
         }
      }
   }

   void stop()
   {
      running_ = false;
      queueConditionVar_.notify_one();
      if (threadConsuming_.joinable()) {
         threadConsuming_.join();
      }
   }
};

#endif
