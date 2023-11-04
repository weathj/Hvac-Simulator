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
};

// Set Commands
class SetAHUSATempCommand : public Command {
public:
    float executeTemp(Building& building, float temp) override {
        float temp = building.setTemp(building.AHU.sa, temp);
        return temp;
    }

    bool executeBool(Building& building) override {
        return false;
    }
};

