#ifndef ROTATIONMOTOR_H
#define ROTATIONMOTOR_H

class RotationMotor {
    public:
        RotationMotor();
        RotationMotor &operator=(const RotationMotor &other) = delete;
        RotationMotor (const RotationMotor &other) = delete;
        ~RotationMotor() = default;
        //Velocity functions
        void setVelocity(int Velocity);
        int getVelocity();
        void incVelocity(int gain);
        void decVelocity(int les);
        //Radius function
        void setRadius(int Radius);
        int getRadius();
        void incRadius(int gain);
        void decRadius(int dec);
        
        void reset();
    private:
        int Velocity_;
        int Radius_;
};

#endif