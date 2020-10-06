#ifndef COLLISIONDETECTOR_H
#define COLLISIONDETECTOR_H

#include <stdio.h>
#include <unistd.h>			//Used for UART
#include <fcntl.h>			//Used for UART
#include <termios.h>	    //Used for UART

class CollisionDetector {
    public: 
        CollisionDetector(int fd);
        ~CollisionDetector() = default;
        void ReadSensor(void);
        bool IsDropCaster(void);
        bool IsDropLeft(void);
        bool IsDropRight(void);
        bool IsBumpLeft(void);
        bool IsBumpRight(void);
    private:
        bool WheeldropCaster;
        bool WheeldropLeft;
        bool WheeldropRight;
        bool BumpLeft;
        bool BumpRight;
        int fd_;
};

#endif