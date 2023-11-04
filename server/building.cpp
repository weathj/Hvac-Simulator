#include "hvac.h"
#include <iostream>
#include <list>

using namespace std;

class Room{
    public:
        string name = "Untitled Room";
        Air air;
        float height = 10;
        float width = 10;
        float length = 10;
        float volume;

        Room::Room(string name, float height, float width, float length){
            this -> name = name;
            this -> air = Air();
            this->height = height;
            this->width = width;
            this->length = length;
            float volume = CalculateVolume();
        }

        float CalculateVolume(){
            return height * width * length;
        }

        void setTemp(float temp){
            this -> air.temp = temp;
        }
    
};

AirUnit AHUBuild(){
    // Outdoor Air
    Air oaAir = Air::Air();

    // Air Handler Setup
    Air saAir = Air();
    Air maAir = Air();
    Air raAir = Air();
    Air buildingAir = Air();

    // Supply Fan
    Fan supplyFan = Fan::Fan(200,800);

    // Return Fan
    Fan returnFan = Fan::Fan(200,800);

    // Dampers
    Damper maDamper = Damper::Damper(5,10);
    Damper oaDamper = Damper::Damper(5,10);
    Damper raDamper = Damper::Damper(5,10);

    // Coils
    Coil coolingCoil = Coil::Coil(5,5);
    Coil heatingCoil = Coil::Coil(5,5);


    // Provide necessary arguments to the constructor of AirUnit
    AirUnit AHU = AirUnit::AirUnit(saAir, maAir, raAir, supplyFan, returnFan, maDamper, raDamper, oaDamper, coolingCoil, heatingCoil);

    return AHU;
};

class Building{
    public:
        bool occupied;
        list<Room> room{};
        Air oa = Air();
        AirUnit AHU = AHUBuild();

        Building(){
            this->AHU = AHU;
            this-> oa.temp = 80;
        }

        void AddRoom(Room room){
            this->room.push_back(room);
        }

        // void RemoveRoom(Room room){
        //     this->room.remove(room);
        // }

        float getTemp(Air air){
            return air.temp;
        }

        float setTemp(Air air, float temp){
            air.temp = temp;
            return air.temp;
        }

        float getDprPos(Damper damper){
            return damper.getPosition();
        }

        float setDprPos(Damper damper, float position){
            damper.setPosition(position);
            return damper.getPosition();
        }

        float getFanSpeed(Fan fan){
            return fan.getSpeed();
        }

        float setFanSpeed(Fan fan, float speed){
            fan.setSpeed(speed);
            return fan.getSpeed();
        }

        float getCoilTemp(Coil coil){
            return coil.temp;
        }

        float setCoilTemp(Coil coil, float temp){
            coil.temp = temp;
            return coil.temp;
        }

        void SetOccupied(bool occupied){
            this->occupied = occupied;
        }

        void SetUnoccupied(){
            this->occupied = false;
        }

        void SetAirHandler(AirUnit AHU){
            this->AHU = AHU;
        }

};

int main() {

    Building building = Building();

    cout << "Supply Air CFM: " << building.AHU.sa.cfm << endl;
    cout << "Supply Air BTU: " << building.AHU.sa.btu << endl;

    // Set Coil Temps
    building.AHU.coolingCoil.temp = 45;
    building.AHU.heatingCoil.temp = 0;

    // Set Temps
    building.AHU.ra.temp = 72;
    building.AHU.oa.temp = 89;

    // Set Damper Positions
    building.AHU.maDamper.Close();
    building.AHU.oaDamper.setPosition(40);
    building.AHU.maDamper.setPosition(100 - building.AHU.oaDamper.getPosition());
    
    // Create room Air
    Room room("Lobby", 10, 20, 30);
    room.air.temp = 70;
    room.air.cfm = 2000;

    // Set fan speeds
    building.AHU.supplyFan.setSpeed(100);
    building.AHU.returnFan.setSpeed(50);
    room.air.temp = building.AHU.HeatCool(room.air);

    // Write a function to display room values and Air handler values
    // Write a function to set room values and Air handler values


    while(true){
        // Temp UI
        cout << endl;
        cout << "_______Temp UI________" << endl;
        cout << "Room Temp: " << room.air.temp << endl;
        cout << "Supply Air Temp: " << building.AHU.sa.temp << endl;
        cout << "Return Air Temp: " << building.AHU.ra.temp << endl;
        cout << "Outdoor Air Temp: " << building.AHU.oa.temp << endl;

        // print all the values
        cout << endl;
        cout << endl;
        cout << "______________________________" << endl;
        cout << "AHU Values: " << endl;
        cout << "------------------------------" << endl;

        //Temperatures
        cout << endl;
        cout << "Temperatures______________" << endl;
        cout << "Supply Air Temp: " << building.AHU.sa.temp << endl;
        cout << "Return Air Temp: " << building.AHU.ra.temp << endl;
        cout << "Outdoor Air Temp: " << building.AHU.oa.temp << endl;
        cout << "Room Temp: " << room.air.temp << endl;

        // CFMs
        cout << endl;
        cout << "_______CFM________" << endl;
        cout << "Supply Air CFM: " << building.AHU.sa.cfm << endl;
        cout << "Return Air CFM: " << building.AHU.ra.cfm << endl;
        cout << "Outdoor Air CFM: " << building.AHU.oa.cfm << endl;


        // BTUs
        cout << endl;
        cout << "_______BTUs_______" << endl;
        cout << "Supply Air BTU: " << building.AHU.sa.btu << endl;
        cout << "Return Air BTU: " << building.AHU.ra.btu << endl;
        cout << "Outdoor Air BTU: " << building.AHU.oa.btu << endl;
        cout << "Room BTU: " << room.air.btu << endl;

        // Damper Positions
        cout << endl;
        cout << "_______Damper Positions________" << endl;
        cout << "Mixed Air Damper Position: " << building.AHU.maDamper.getPosition() << endl;
        cout << "Outdoor Air Damper Position: " << building.AHU.oaDamper.getPosition() << endl;

        // Fan Speeds
        cout << endl;
        cout << "_______Fan Speeds________" << endl;
        cout << "Supply Fan Speed: " << building.AHU.supplyFan.getSpeed() << endl;
        cout << "Return Fan Speed: " << building.AHU.returnFan.getSpeed() << endl;

        // Coil Temps
        cout << endl;
        cout << "_______Coil Temps________" << endl;
        cout << "Cooling Coil Temp: " << building.AHU.coolingCoil.temp << endl;
        cout << "Heating Coil Temp: " << building.AHU.heatingCoil.temp << endl;

        cout << endl;
        cout << "______________________________" << endl;
        cout << "What would you like to do?" << endl;
        cout << "1. Set Supply Fan Speed" << endl;
        cout << "2. Set Return Fan Speed" << endl;
        cout << "3. Set Mixed Air Damper Position" << endl;
        cout << "4. Set Outdoor Air Damper Position" << endl;
        cout << "5. Set Room Temperature" << endl;

        int choice;
        cin >> choice;

        if (choice == 1){
            cout << "Enter Supply Fan Speed: ";
            int speed;
            cin >> speed;
            building.AHU.supplyFan.setSpeed(speed);
        } else if (choice == 2){
            cout << "Enter Return Fan Speed: ";
            int speed;
            cin >> speed;
            building.AHU.returnFan.setSpeed(speed);
        } else if (choice == 3){
            cout << "Enter Mixed Air Damper Position: ";
            int position;
            cin >> position;
            building.AHU.maDamper.setPosition(position);
        } else if (choice == 4){
            cout << "Enter Outdoor Air Damper Position: ";
            int position;
            cin >> position;
            building.AHU.oaDamper.setPosition(position);
        } else if (choice == 5){
            cout << "Enter Room Temperature: ";
            int temp;
            cin >> temp;
            room.setTemp(temp);
        } else {
            cout << "Invalid Choice" << endl;
        } 
    }

    building.AHU.HeatCool(room.air);

    return 0;
}