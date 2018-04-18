import json
import bluetooth
import threading
import timed_LEDs
import subprocess
import ast

def start_laps(delay, lap_times):
    timed_LEDs.start_LEDs(delay, lap_times)


# put pi in discoverable 
subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_socket.bind(("", port))
server_socket.listen(1)

client_socket, address = server_socket.accept()
print("Accepted connection from ", address)

threads = []
while True:
    print("RECEIVING")
    data = client_socket.recv(1024)
    data = json.loads(data.decode())
    print(data)
    if(data["lap_times"]):
        print("STARTING THREAD")
        t = threading.Thread(target=start_laps(int(data["delay"]), ast.literal_eval(data["lap_times"])))
        threads.append(t)
        t.start()
    elif data == "stop":
        print("Stop dat lap doh")
    else: 
        print(data)


client_socket.close()

