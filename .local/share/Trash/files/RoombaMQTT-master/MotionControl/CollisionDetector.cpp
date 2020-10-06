#include "CollisionDetector.h"
#include <iostream>

CollisionDetector::CollisionDetector(int fd)
    : fd_(fd), WheeldropCaster(false), WheeldropLeft(false), WheeldropRight(false)
    , BumpLeft(false), BumpRight(false) {
    //CONFIGURE THE UART
	//The flags (defined in /usr/include/termios.h - see http://pubs.opengroup.org/onlinepubs/007908799/xsh/termios.h.html):
	//	Baud rate:- B1200, B2400, B4800, B9600, B19200, B38400, B57600, B115200, B230400, B460800, B500000, B576000, B921600, B1000000, B1152000, B1500000, B2000000, B2500000, B3000000, B3500000, B4000000
	//	CSIZE:- CS5, CS6, CS7, CS8
	//	CLOCAL - Ignore modem status lines
	//	CREAD - Enable receiver
	//	IGNPAR = Ignore characters with parity errors
	//	ICRNL - Map CR to NL on input (Use for ASCII comms where you want to auto correct end of line characters - don't use for bianry comms!)
	//	PARENB - Parity enable
	//	PARODD - Odd parity (else even)
    struct termios options;
    tcgetattr(fd_, &options);
    options.c_cflag = B115200 | CS8 | CLOCAL | CREAD;
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(fd_, TCIFLUSH);
    tcsetattr(fd_, TCSANOW, &options);
}

void CollisionDetector::ReadSensor(void) {
    uint8_t opcode{142};
    uint8_t sensorID{7};
    uint8_t p_tx_buffer[2] = {opcode, sensorID};

    int count = write(fd_, (void*)p_tx_buffer, 2);
    if (count == -1) {
        std::cerr<<"UART TX error"<<std::endl;
    }

    uint8_t rx_buffer[256];
    int rx_length = read(fd_, (void*)rx_buffer, 255);
    if (rx_length < 0) {
        //Error
    }
    else if (rx_length == 0) {
        std::cerr<<"There is no data to read"<<std::endl;
    }
    else {
        write(1, (void*)rx_buffer, rx_length);
    }
}
bool CollisionDetector::IsDropCaster(void) {
    return WheeldropCaster;
}
bool CollisionDetector::IsDropLeft(void) {
    return WheeldropLeft;
}
bool CollisionDetector::IsDropRight(void) {
    return WheeldropRight;
}
bool CollisionDetector::IsBumpLeft(void) {
    return BumpLeft;
}
bool CollisionDetector::IsBumpRight(void) {
    return BumpRight;
}