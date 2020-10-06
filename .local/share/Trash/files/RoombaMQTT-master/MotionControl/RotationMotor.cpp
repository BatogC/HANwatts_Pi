#include "RotationMotor.h"
#include <iostream>

RotationMotor::RotationMotor() : Velocity_(0), Radius_(0) {
    std::cout<<"A rotation motor has been created with ID: "<<std::endl;
}

void RotationMotor::setVelocity(int Velocity) {
    Velocity_=Velocity;
}

int RotationMotor::getVelocity() {
    return Velocity_;
}

void RotationMotor::incVelocity(int gain) {
    Velocity_+=gain;
}

void RotationMotor::decVelocity(int dec) {
    Velocity_-=dec;
}

void RotationMotor::setRadius(int Radius) {
    Radius_=Radius;
}

int RotationMotor::getVelocity() {
    return Radius_;
}

void RotationMotor::incVelocity(int gain) {
    Radius_+=gain;
}

void RotationMotor::decVelocity(int dec) {
    Radius_-=dec;
}

void RotationMotor::reset() {
    setVelocity(0);
    setRadius(0);
}