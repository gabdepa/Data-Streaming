import socket
import json

server_address = "127.0.0.1"
# server_address = str(input("Enter the server address:"))
port = 12345

# Inicialização do socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Envia solicitação de registro no servidor
client_socket.sendto("register".encode(), (server_address, port))

with open("client.log", "a") as f:
    f.write(f"(client) Client connected to server {server_address} on port {port}.\n")

lost_packets = 0 # Número de pacotes perdidos
out_of_order = 0 # Número de pacotes fora de ordem
last_received = 0 # Número do último pacote recebido
received_packets = 0  # Contador de pacotes recebidos
first_packet_received = True  # Flag para verificar se é o primeiro pacote recebido

def generateClientStats(receivedEndOfTransmission):
    with open("client_stats.log", "a") as f:
        if receivedEndOfTransmission:
            f.write("\n(client) Received end of transmission.")
        else : 
            f.write("\n(client) Ctrl+C received. Unregistering client.")

        # Dados de estatística de streaming
        f.write(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> STATISTICS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<< \n")
        f.write(f"(client) Number of packets received: {received_packets} \n")
        f.write(f"(client) Number of lost packets: {lost_packets} \n")
        f.write(f"(client) Number of packets out of order: {out_of_order}\n")

try:
    while True:
        # Recebe mensagem e endereço do socket
        message, address = client_socket.recvfrom(1024)
        
        if message.decode() == "End of transmission":
            print('*'*80)
            print('Fim de jogo!')
            print('*'*80)

            generateClientStats(True)
            break

        # Converte a mensagem JSON para um dicionário Python
        message_dict = json.loads(message.decode())
        
        # Acessa o contador da mensagem
        current_order = message_dict["message"]["count"]
        # Se for o primeiro pacote
        if first_packet_received:
            # Define a flag para False
            first_packet_received = False
            # Inicialize o contador de pacotes recebidos
            received_packets = 1        
            last_received = current_order
        # Se não for o primeiro pacote
        else:
            # Incremente o contador de pacotes recebidos
            received_packets += 1
        
        # Estatísticas 
        if current_order < last_received:
            out_of_order += 1
        elif current_order > last_received + 1:
            lost_packets += (current_order - last_received - 1)
        
        # Implementar alguma operação nos dados recebidos......
        with open("client.log", "a") as f:
            f.write(f"(client) Received message: {message_dict} from {address} \n") 
        
        print("\n")
        print('*'*80)
        print(message_dict['message']['content'])
        print(message_dict['message']['type'])
        print(message_dict['message']['score'])
        print(message_dict['message']['time_passed'])
        print('*'*80)
        # Atualiza o último pacote recebido
        last_received = current_order

# Caso cliente seja interrompido
except KeyboardInterrupt:
    # Envia mensagem de cancelamento de registro ao servidor
    client_socket.sendto("unregister".encode(), (server_address, port))

    generateClientStats(False)

