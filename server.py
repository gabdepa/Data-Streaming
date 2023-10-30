import socket
import time
import threading
import json 

import simulate_game
import random

port = 12345

TOTAL_EVENTOS_JOGO = random.randint(30, 100)

# Simula uma partida
jogo_simulado = simulate_game.simular_partida(TOTAL_EVENTOS_JOGO)

# Enviar mensagem para um cliente
def send_message_to_client(event, client_address, server_socket):
    with open("server.log", "a") as f:
        f.write(f"(server) Sending message to client {client_address}")

    # Cria um dicionário para a mensagem
    message= {"count": count, "score": jogo_simulado[count][0],"content": jogo_simulado[count][1], "type": jogo_simulado[count][2]} # added type to datagram, which is the type of the event of the stream   
    # Converte o dicionário para uma string JSON
    json_message = json.dumps({"message": message })  
    # Espera pelo sinal para enviar a mensagem
    event.wait()  
    # Codifica a string JSON antes de enviar via socket
    server_socket.sendto(json_message.encode(), client_address) 

# Lida com registros de clientes
def handle_client_registration(server_socket, clients):
    while True:
        message, address = server_socket.recvfrom(1024)
        with open("server.log", "a") as f:
            f.write(f"\n(server) Received {message} of address {address} on socket")

            if message.decode() == "register":
                f.write(f"(server) Registering client {address}. \n")
                clients.add(address)
            elif message.decode() == "unregister":
                f.write(f"(server) Unregistering client {address}. \n")
                clients.discard(address)

            f.write(f"(server) Number of clients registered: {len(clients)}\n")
 
# Define tempo de intervalo entre envio de notificações
user_input = input("Insira o tempo entre os envios de notificações: ")
sleepTime = int(user_input)

# Inicialização do socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", port))  # Escuta em todas as interfaces de rede

with open("server.log", "a") as f:
    f.write(f"(server) Server started on port {port}. \n")

# Conjunto de clientes
clients = set()

# Contador de pacotes totais enviados
count = 0

# Inicializa nova thread para lidar com registro de clientes
client_registration_thread = threading.Thread(target=handle_client_registration, args=(server_socket,clients))
client_registration_thread.start()

while count < TOTAL_EVENTOS_JOGO:
    # Preparação para enviar o mesmo pacote para todos os clientes ao mesmo tempo
    event = threading.Event()
    threads = []
    
    # Para cada cliente registrado para receber mensagens
    for client in clients:
        # Cria thread para enviar a mensagem
        thread = threading.Thread(target=send_message_to_client, args=(event, client, server_socket))
        # Adiciona thread no vetor de threads
        threads.append(thread)
        # Thread começa a rodar   
        thread.start()
    
    # Intervalo de tempo entre cada mensagem 
    time.sleep(sleepTime)  

    # Dispara o sinal para todos as threads enviarem a mensagem
    event.set()  

    # Garante que todas as mensagens sejam enviadas antes que o loop continue
    for thread in threads:
        thread.join()
    
    # Incrementa contador de mensagem enviada
    count += 1

for cAddr in clients:
    with open("server.log", "a") as f:
        f.write(f"(server) Sended end of transmission message. \n")
    server_socket.sendto("End of transmission".encode(), cAddr)


client_registration_thread.interrupt()