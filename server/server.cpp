#include <boost/asio.hpp>
#include <nlohmann/json.hpp>
#include <iostream>
#include "hvac.h"
#include "building.h"
#include "command.h"

using boost::asio::ip::tcp;
using namespace std;
using namespace boost::asio;
using json = nlohmann::json;

// class HVACSimulator {
// public:
//     float setTemperature(float temp) {
//         Air air = Air();
//         air.temp = temp;
//         return air.temp;
//     }
//     // Add more functionality like startingFans, Opening Dampers, etc.
//     // ... 
// };

void handle_client(tcp::socket& socket, Building building) {
    try {
        boost::asio::streambuf buf;
        boost::system::error_code error;

        cout << "Reading from client." << endl;

        boost::asio::read_until(socket, buf, "\n", error);

        if (!error) {
            std::istream is(&buf);
            std::string requestData;
            std::getline(is, requestData);
            cout << "Received data: " << requestData << endl;
            json request = json::parse(requestData);
            json response;

            // Check for various commands and respond accordingly
            // Get commands
            if (request.contains("getAHUSATemp")) {
                GetAHUSATempCommand saTempCommand;
                response["AHUSATemp"] = saTempCommand.executeFloat(building);
                cout << "Response Sent" << endl;
            } else if (request.contains("getAHURATemp")) {
                GetAHURATempCommand raTempCommand;
                response["AHURATemp"] = raTempCommand.executeFloat(building);
                cout << "Response Sent" << endl;
            } else if (request.contains("getOATemp")) {
                GetOATempCommand oaTempCommand;
                response["OATemp"] = oaTempCommand.executeFloat(building);
                cout << "Response Sent" << endl;
            } else if (request.contains("getMADPRPos")) {
                GetAHUMADPRPosCommand maDprPosCommand;
                response["MADPRPos"] = maDprPosCommand.executeFloat(building);
                cout << "Response Sent" << endl;
            } else if (request.contains("getOADPRPos")) {
                GetAHUOADPRPosCommand oaDprPosCommand;
                response["OADPRPos"] = oaDprPosCommand.executeFloat(building);
                cout << "Response Sent" << endl;
            } else if (request.contains("getSAFANSpeed")) {
                GetAHUSAFANSpeedCommand saFanSpeedCommand;
                response["SAFANSpd"] = saFanSpeedCommand.executeFloat(building);
                cout << "Response Sent" << endl;
            } else if (request.contains("getRAFANSpeed")) {
                GetAHURAFANSpeedCommand raFanSpeedCommand;
                response["RAFANSpd"] = raFanSpeedCommand.executeFloat(building);
                cout << "Response Sent" << endl;
            } else if (request.contains("getCLGCOILTemp")) {
                GetAHUCoolingCoilTempCommand clgCoilTempCommand;
                response["CLGCOILTemp"] = clgCoilTempCommand.executeFloat(building);
                cout << "Response Sent" << endl;
            } else if (request.contains("getHTGCOILTemp")) {
                GetAHUHeatingCoilTempCommand htgCoilTempCommand;
                response["HTGCOILTemp"] = htgCoilTempCommand.executeFloat(building);
                cout << "Response Sent" << endl;
            } 

            // Set commands
            else if (request.contains("setAHUSATemp")) {
                SetAHUSATempCommand saTempCommand;  
                float temp = request["setAHUSATemp"];

                saTempCommand.executeTemp(building, temp);
                response["AHUSATemp"] = temp;
                cout << "Response Sent" << endl;
            }


            // Send response
            std::string response_str = response.dump() + "\n";
            boost::asio::write(socket, boost::asio::buffer(response_str), error);

        }
        else {
            cout << "Error reading from client: " << error.message() << endl;
        }
    }
    catch (const std::exception& e) {
        cerr << "Error handling client: " << e.what() << endl;
    }
}

int main() {
    io_context io_context;
    tcp::acceptor acceptor(io_context, tcp::endpoint(ip::address_v4::loopback(), 7880));
    Building building = Building();
    building.AHU.sa.temp = 123;
    building.AHU.ra.temp = 456;
    building.oa.temp = 789;
    building.AHU.maDamper.setPosition(0.5);
    building.AHU.oaDamper.setPosition(0.5);
    building.AHU.supplyFan.setSpeed(0.5);
    building.AHU.returnFan.setSpeed(0.5);
    building.AHU.coolingCoil.temp = 123;
    building.AHU.heatingCoil.temp = 456;
    cout << "SA Temp: " << building.AHU.sa.temp << endl;

    cout << "Server is running..." << endl;

    while (true) {
        tcp::socket socket(io_context);
        acceptor.accept(socket);
        cout << "Client connected: " << socket.remote_endpoint() << endl;
        handle_client(socket, building);
        building.AHU.HeatCool(building.oa);
    }

    return 0;
}
