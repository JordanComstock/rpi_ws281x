import json
import bluetooth
import threading
import timed_LEDs


server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_socket.bind(("", port))
server_socket.listen(1)

client_socket, address = server_socket.accept()
print("Accepted connection from ", address)

threads = []
while True:
    data = client_socket.recv(1024)
    data = json.loads(data.decode())
    if(data["lap_times"]):
        t = threading.Thread(target=start_laps(int(data["delay"]), data["lap_times"]))
        threads.append(t)
        t.start()

client_socket.close()

def start_laps(delay, lap_times):
    timed_LEDs.start_LEDs(delay, lap_times)
