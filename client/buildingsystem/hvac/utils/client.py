import socket
import json
import time

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Attempting to connect to server...")
        self.socket.connect((self.ip, self.port))
        print("Connected to server:", self.ip, "on port:", self.port)

    def send(self, data):
        ## Send data to server
        print("Sending data:", data)
        self.socket.send(data.encode())
        print("Data sent.")

    def receive(self):
        try:
            print("Waiting for server response...")
            data = self.socket.recv(1024).decode()
            if not data:
                print("Server closed the connection.")
                return None
            print("Received data:", data)
            return data
        except socket.error as e:
            print(f"Socket error: {e}")
            return None

    def close(self):
        print("Closing connection.")
        self.socket.close()

    def request(self, data):
        self.send(json.dumps(data) + "\n")
        response = self.receive()
        return json.loads(response)

    def start_interaction(self):
        while True:
            # Ui
            action = input("Enter action (e.g., 'setTemperature', 'startFans', 'exit' to quit): ")

            if action == "exit":
                break

            if action == "setTemperature":
                temp = float(input("Enter desired temperature: "))
                data = {"setTemperature": temp}
            elif action == "startFans":
                # Add other parameters if needed
                data = {"startFans": True}
            # ... Add other actions here

            response = self.request(data)
            print("Server response:", response)

if __name__ == "__main__":
    data = {
        "getOA": True
    }

    # Use this pattern whenever you want to communicate:
    client = Client("127.0.0.1", 7880)
    client.send(json.dumps(data) + "\n")
    time.sleep(0.1)  # wait for 100 milliseconds
    response_data = client.receive()
    if response_data:
        response = json.loads(response_data)
        print("Received:", response)
    else:
        print("No data received from server or there was an error.")
    client.close()