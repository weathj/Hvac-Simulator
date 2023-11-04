#ifndef BUILDING_H
#define BUILDING_H

#include <iostream>
#include <list>
#include "hvac.h"

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

class Building{
    public:
        bool occupied;
        list<Room> room{};
        Air oa = Air();
        AirUnit AHU;

        Building(){
            this->AHU = AHU;
        }

        void AddRoom(Room room){
            this->room.push_back(room);
        }

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

        // void RemoveRoom(Room room){
        //     this->room.remove(room);
        // }

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
#endif // BUILDING_H