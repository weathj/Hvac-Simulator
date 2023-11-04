#ifndef COMMAND_H
#define COMMAND_H

#include "building.h"

using namespace std;

class Command {
public:
    virtual float executeFloat(Building& building) = 0;
    virtual bool executeBool(Building& building) = 0;
    virtual float executeTemp(Building& building, float temp) = 0;
};

// Concrete command classes

// Get Commands
class GetAHUSATempCommand : public Command {
public:
    float executeFloat(Building& building) override {
        float temp = building.getTemp(building.AHU.sa);
        return temp;
    }

    bool executeBool(Building& building) override {
        return false;
    }

    float executeTemp(Building& building, float temp) override {
        return 0;
    }
};

class GetAHURATempCommand : public Command {
public:
    float executeFloat(Building& building) override {
        float temp = building.getTemp(building.AHU.ra);
        return temp;
    }

    bool executeBool(Building& building) override {
        return false;
    }
    
    float executeTemp(Building& building, float temp) override {
        return 0;
    }
};

class GetOATempCommand : public Command {
public:
    float executeFloat(Building& building) override {
        float temp = building.getTemp(building.oa);
        return temp;
    }

    bool executeBool(Building& building) override {
        return false;
    }

    float executeTemp(Building& building, float temp) override {
        return 0;
    }
};

class GetAHUMADPRPosCommand : public Command {
public:
    float executeFloat(Building& building) override {
        float pos = building.getDprPos(building.AHU.maDamper);
        return pos;
    }

    bool executeBool(Building& building) override {
        return false;
    }

    float executeTemp(Building& building, float temp) override {
        return 0;
    }
};

class GetAHUOADPRPosCommand : public Command {
public:
    float executeFloat(Building& building) override {
        float pos = building.getDprPos(building.AHU.oaDamper);
        return pos;
    }

    bool executeBool(Building& building) override {
        return false;
    }

    float executeTemp(Building& building, float temp) override {
        return 0;
    }
};

class GetAHUSAFANSpeedCommand : public Command {
public:
    float executeFloat(Building& building) override {
        float speed = building.getFanSpeed(building.AHU.supplyFan);
        return speed;
    }

    bool executeBool(Building& building) override {
        return false;
    }

    float executeTemp(Building& building, float temp) override {
        return 0;
    }
};

class GetAHURAFANSpeedCommand : public Command {
public:
    float executeFloat(Building& building) override {
        float speed = building.getFanSpeed(building.AHU.returnFan);
        return speed;
    }

    bool executeBool(Building& building) override {
        return false;
    }

    float executeTemp(Building& building, float temp) override {
        return 0;
    }
};

class GetAHUCoolingCoilTempCommand : public Command {
public:
    float executeFloat(Building& building) override {
        float temp = building.getCoilTemp(building.AHU.coolingCoil);
        return temp;
    }

    bool executeBool(Building& building) override {
        return false;
    }

    float executeTemp(Building& building, float temp) override {
        return 0;
    }
};

class GetAHUHeatingCoilTempCommand : public Command {
public:
    float executeFloat(Building& building) override {
        float temp = building.getCoilTemp(building.AHU.heatingCoil);
        return temp;
    }

    bool executeBool(Building& building) override {
        return false;
    }

    float executeTemp(Building& building, float temp) override {
        return 0;
    }
};

// Set Commands
class SetAHUSATempCommand : public Command {
public:
    float executeTemp(Building& building, float temp) override {
        float new_temp = temp;
        new_temp = building.setTemp(building.AHU.sa, new_temp);
        return new_temp;
    }

    bool executeBool(Building& building) override {
        return false;
    }

    float executeFloat(Building& building) override {
        return 0;
    }
};



#endif // COMMAND_H