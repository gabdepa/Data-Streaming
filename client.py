import socket
import json

# server_address = str(input("Enter the server address:"))
server_address = "127.0.0.1"

# Inicialização do socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto("register".encode(), (server_address, 12345))

lost_packets = 0 # Número de pacotes perdidos
out_of_order = 0 # Número de pacotes fora de ordem
last_received = 0 # Número do último pacote recebido
received_packets = 0  # Contador de pacotes recebidos
first_packet_received = True  # Flag para verificar se é o primeiro pacote recebido

try:
    while True:
        # Recebe mensagem e endereço do socket
        message, address = client_socket.recvfrom(1024)
        
        # Converte a mensagem JSON para um dicionário Python
        message_dict = json.loads(message.decode())
        
        # Acessa o contador da mensagem
        current_order = message_dict["message"]["count"]
        if first_packet_received:
            # Se for o primeiro pacote, inicialize o contador e defina a flag para False
            first_packet_received = False
            received_packets = 1        
            last_received = current_order
        else:
            # Se não for o primeiro pacote, incremente o contador
            received_packets += 1
        
        # Estatísticas (simples)
        if current_order < last_received:
            out_of_order += 1
        elif current_order > last_received + 1:
            lost_packets += (current_order - last_received - 1)
        
        # Implementar alguma operação nos dados recebidos
        print(f"(client) Received: {message_dict} from {address}") 
        # Dados de streaming
        print(f"(client) number of packets received: {received_packets}")
        print(f"(client) number of lost packets: {lost_packets}")
        print(f"(client) number of packets out of order: {out_of_order}\n")
        
        # Atualize o último pacote recebido
        last_received = current_order

except KeyboardInterrupt:
    print("(client) Ctrl+C received. Unregistering client.")
    client_socket.sendto("unregister".encode(), (server_address, 12345))
