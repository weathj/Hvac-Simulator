#include <iostream>
#include <cstring> // for string class

using namespace std;

class Air {
    public:
        float temp;
        float humidity;
        float density = 0.075f; // lb/ft^3
        float heat_capacity = 1.08f; // BTU/lb-F, Product of Specific Heat (0.24 BTU) and Density (0.075 lbs cubic foot) times the number of minutes per hour (60)
        float cfm;
        float specific_heat = 0.24f; // BTU/lb-F
        float btu; // BTU per minute (Scaled down for 1 minute for simulation purposes)
        float pressure = 0.4f; // in WC

        float CalculateBTU(float supply_temp){
            float temp_change = (supply_temp - this -> temp) / 60; // Temp change per minute
            cout << "Temp Change: " << temp_change << endl;

            // if (temp > air.temp) {
            //     temp_change = temp_change * -1;

            float mass_flow = cfm * density;
            float btu = mass_flow * specific_heat * temp_change; // BTU per minute
            cout << "BTU: " << btu << endl;

            if (supply_temp < temp) {
                btu = btu * -1;
            }

            return btu;
        }

        float CalculatePressure(float pressure, float incoming_cfm, float volume){
            float cfm_offset = abs(cfm - incoming_cfm);
            float air_change_rate = (cfm_offset * 60) / volume; // ACH due to offset
            float volume_change = (volume * air_change_rate) / 60; // Volume change in one minute
            float new_volume = volume + volume_change;
            float p2 = pressure * (volume / new_volume);
            return p2 - pressure;
        }

};

class Fan {
    private:
        float speed; // 0-100 Percentage
        float velocity; // FPM
        float max_velocity; // FPM
        float min_velocity; // FPM

    public:
        bool fanSts;

        Fan(float max_velocity, float min_velocity){
            this->max_velocity = max_velocity;
            this->min_velocity = min_velocity;
        };

        bool turnOn(){
            fanSts = true;
            return fanSts;
        }

        bool turnOff(){
            fanSts = false;
            return fanSts;
        }

        void setSpeed(float speed){
            if (speed > 100) {
                speed = 100;
            } else if (speed < 0) {
                speed = 0;
            }
            this->speed = speed;

            float velocity = (speed / 100) * max_velocity; //FPM - Normalize speed to a percentage between 0 and 10
            if (velocity > max_velocity) {
                this -> velocity = max_velocity;
            } else if (velocity < min_velocity) {
                this -> velocity = min_velocity;
            }
            this->velocity = velocity;
            cout << "Root Velocity: " << velocity << endl;
        }

        float getSpeed(){
            return speed;
        }

        float getVelocity(){
            return velocity;
        }
};

class Damper {
    private:
        float position; // 0-100 Percentage
        float area; // ft^2

    public:
        float height;
        float width;

        Damper(float height, float width){
            this->height = height;
            this->width = width;
        }

        void Open(){
            this -> position = 100;
        }

        void Close(){
            this -> position = 0;
        }

        void setPosition(float position){
            if (position > 100) {
                this -> position = 100;
            } else if (position < 0) {
                this -> position = 0;
            }
            this -> position = position;
            cout << "Root Position: " << position << endl;
        }

        float getPosition(){
            return position;
        }

        // Calculate CFM based on fan velocity and damper size and position
        float getCFM(float velocity){
            area = height * width;
            cout << "Area: " << area << endl;
            cout << "Velocity: " << velocity << endl;
            float cfm = area * velocity;
            cout << "Position: "  << position << endl;
            cout << "Max CFM: " << cfm << endl;
            cfm = cfm * (position / 100);
            cout << "Final CFM: " << cfm << endl;
            return cfm;
        }

};

class Coil{
    private:
        float height;
        float width;
    public:
        float temp;

        Coil(float height, float width){
            this->height = height;
            this->width = width;
        }

        float getArea(){
            return height * width;
        }
};

class AirUnit{
    public:

        // Unit Operation
        bool unitSts;

        // Supply Side
        Air sa = Air();
        Fan supplyFan = Fan(200, 800);
        float supplyAirFlow;
        Coil coolingCoil = Coil(5, 5);
        Coil heatingCoil = Coil(5, 5);
        
        // Mixed Air
        Air ma = Air();

        // Return Side
        Air ra = Air();
        Fan returnFan = Fan(200, 800);
        Damper maDamper = Damper(5, 10);
        float returnAirFlow;

        // Outdoor Air
        Air oa = Air();
        Damper oaDamper = Damper(5, 10);
        float outdoorAirFlow;

        bool TurnOn(){
            unitSts = true;
            return unitSts;
        }

        bool TurnOff(){
            unitSts = false;
            return unitSts;
        }

        float HeatCool(Air room){
            //okay function for now but will need tuned to be more accurate to reality
            
            cout << "Supply Fan Speed: " << supplyFan.getSpeed() << endl;
            cout << "Return Fan Speed: " << returnFan.getSpeed() << endl;
            cout << "Oa Damper Position: " << oaDamper.getPosition() << endl;
            cout << "Ma Damper Position: " << maDamper.getPosition() << endl;

            // Flow
            ra.cfm = maDamper.getCFM(returnFan.getVelocity());
            oa.cfm = oaDamper.getCFM(supplyFan.getVelocity());

            // print speeds
            cout << "Supply Fan Speed: " << supplyFan.getSpeed() << endl;
            cout << "Return Fan Speed: " << returnFan.getSpeed() << endl;

            // print ra and oa flows
            cout << "Return Air CFM: " << ra.cfm << endl;
            cout << "Outdoor Air CFM: " << oa.cfm << endl;

            ma.cfm = ra.cfm + oa.cfm;
            sa.cfm = ma.cfm;

            // Getting BTUs
            room.btu = room.CalculateBTU(sa.temp);
            ra.btu = ra.CalculateBTU(room.temp);

            // Heating/Cooling BTU
            float cooling_btu = coolingCoil.getArea() * (coolingCoil.temp - ma.temp);
            float heating_btu = heatingCoil.getArea() * (heatingCoil.temp - ma.temp);

            // Ensure that the heating btu is positive and cooling btu is negative
            if (cooling_btu > 0) {
                cooling_btu = 0;
            } else if (heating_btu < 0) {
                heating_btu = 0;
            }

            // Calculate temp change
            float cooling_temp_change = cooling_btu / (coolingCoil.getArea() * ma.density * ma.specific_heat) / 30; // 30 is the tie variable
            float heating_temp_change = heating_btu / (heatingCoil.getArea() * ma.density * ma.specific_heat) / 30; // 30 is the time variable


            cout << "Cooling BTU: " << cooling_btu << endl;
            cout << "Heating BTU: " << heating_btu << endl;

            ma.btu = cooling_btu + heating_btu;
            ma.temp = ma.temp + cooling_temp_change + heating_temp_change;

            float oa_ma_btu = ma.CalculateBTU(oa.temp) * maDamper.getPosition() / 100;
            cout << "OA BTU: " << oa_ma_btu << endl;
            float ra_ma_btu = ma.CalculateBTU(ra.temp) * maDamper.getPosition() / 100;
            cout << "RA BTU: " << ra_ma_btu << endl;
            ma.btu = oa_ma_btu + ra_ma_btu;

            // Set supply air values
            sa.btu = ma.btu;
            sa.temp = ma.temp;

            // Calculate room temp change
            float total_btu =  (ra.btu + oa.btu) - (sa.btu + room.btu);
            cout << "Total BTU: " << total_btu << endl;
            float temp_change = total_btu / (1000 * room.density * room.specific_heat) / 30; // 30 is the time variable

            // If supply air is less than room air make temp change negative
            if(sa.temp > room.temp){
                temp_change = temp_change * -1;
            }

            float temp = room.temp + temp_change;
            return temp;
        }

};

int main() {
    AirUnit AHU = AirUnit();
    cout << "Supply Air CFM: " << AHU.sa.cfm << endl;
    cout << "Supply Air BTU: " << AHU.sa.btu << endl;

    // Set Coil Temps
    AHU.coolingCoil.temp = 45;
    AHU.heatingCoil.temp = 0;

    // Set Temps
    AHU.ra.temp = 72;
    AHU.oa.temp = 89;

    // Set Damper Positions
    AHU.maDamper.Close();
    AHU.oaDamper.setPosition(40);
    AHU.maDamper.setPosition(100 - AHU.oaDamper.getPosition());
    
    // Create room Air
    Air room = Air();
    room.temp = 70;
    room.cfm = 2000;

    // Set fan speeds
    AHU.supplyFan.setSpeed(100);
    AHU.returnFan.setSpeed(50);
    room.temp = AHU.HeatCool(room);

    // print all the values
    cout << endl;
    cout << endl;
    cout << "______________________________" << endl;
    cout << "AHU Values: " << endl;
    cout << "------------------------------" << endl;

    //Temperatures
    cout << endl;
    cout << "Temperatures______________" << endl;
    cout << "Supply Air Temp: " << AHU.sa.temp << endl;
    cout << "Return Air Temp: " << AHU.ra.temp << endl;
    cout << "Outdoor Air Temp: " << AHU.oa.temp << endl;
    cout << "Room Temp: " << room.temp << endl;

    // CFMs
    cout << endl;
    cout << "_______CFM________" << endl;
    cout << "Supply Air CFM: " << AHU.sa.cfm << endl;
    cout << "Return Air CFM: " << AHU.ra.cfm << endl;
    cout << "Outdoor Air CFM: " << AHU.oa.cfm << endl;


    // BTUs
    cout << endl;
    cout << "_______BTUs_______" << endl;
    cout << "Supply Air BTU: " << AHU.sa.btu << endl;
    cout << "Return Air BTU: " << AHU.ra.btu << endl;
    cout << "Outdoor Air BTU: " << AHU.oa.btu << endl;
    cout << "Room BTU: " << room.btu << endl;

    // Damper Positions
    cout << endl;
    cout << "_______Damper Positions________" << endl;
    cout << "Mixed Air Damper Position: " << AHU.maDamper.getPosition() << endl;
    cout << "Outdoor Air Damper Position: " << AHU.oaDamper.getPosition() << endl;

    // Fan Speeds
    cout << endl;
    cout << "_______Fan Speeds________" << endl;
    cout << "Supply Fan Speed: " << AHU.supplyFan.getSpeed() << endl;
    cout << "Return Fan Speed: " << AHU.returnFan.getSpeed() << endl;

    return 0;
}