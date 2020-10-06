#ifndef PILOT_H
#define PILOT_H

#include "RotationMotor.h"

class Pilot {
    public:
        Pilot(int fd);
        ~Pilot() = default;
    private:
        int fd_;
        RotationMotor Motor_R;
        RotationMotor Motor_L;
};

#endif