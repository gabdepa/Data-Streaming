import socket
import json


server_address = input("Enter the server address:")

# Inicialize o socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto("register".encode(), (str(server_address), 12345))

received_packets = 0
lost_packets = 0
out_of_order = 0
last_received = 0

while True:
   # Recebe mensagem e endereço do socket
    message, address = client_socket.recvfrom(1024)
    
    # Converte a mensagem JSON para um dicionário Python
    message_dict = json.loads(message.decode())
    print(f"(client) Received: {message_dict} from {address}")

    # Contador de pacotes
    received_packets += 1
    
    # Implementar alguma operação nos dados recebidos
    # Por exemplo, imprimir a mensagem
    print(f"(client) Received: {message_dict} from {address}")
    
    # Estatísticas (simples)
    # Agora, use os campos do dicionário para estatísticas ou qualquer outra operação
    current_order = message_dict["message"]["count"]  # Aqui estamos acessando o campo "count" do dicionário
    if current_order < last_received:
        out_of_order += 1
    elif current_order > last_received + 1:
        lost_packets += (current_order - last_received - 1)
    
    print(f"(client) lost packets: {lost_packets}")
    print(f"(client) number of packets out of order: {out_of_order}\n")
    last_received = current_order
