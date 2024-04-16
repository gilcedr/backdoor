from vidstream import StreamingServer
import threading

HOST_IP = StreamingServer('127.0.0.1', 30000)
thread = threading.Thread(target=HOST_IP.start_server)

thread.start()

while input("") != "stop" :
    continue

HOST_IP.stop_server()