import socket
import time
import threading
import json 
import simulate_game
import random
from simulate_game import jogadores_casa 
from simulate_game import goleiro_time_casa
from simulate_game import jogadores_visitante 
from simulate_game import goleiro_time_visitante

# Converte uma lista de objetos Jogador para uma lista de dicionários
def jogador_to_dict(jogadores):
    return [{"nome": jogador.nome, "time": jogador.time, "posicao": jogador.posicao, "cartao_vermelho": jogador.cartao_vermelho, "gols": jogador.gols, "tempo_gols": jogador.tempo_gols, "tempo_cv": jogador.tempo_cv} for jogador in jogadores]

# Enviar mensagem para um cliente
def send_events_message_to_client(event, client_address, server_socket):
    with open("server.log", "a") as f:
        f.write(f"\n(server) Sending message to client {client_address}")

    # Cria um dicionário para a mensagem
    message1 = {"count": count, "score": jogo_simulado[count][0],"content": jogo_simulado[count][1], "type": jogo_simulado[count][2], "time_passed": jogo_simulado[count][3]} # added type to datagram, which is the type of the event of the stream   
    timeA = jogador_to_dict(jogadores_casa)
    goleiroA = {"nome": goleiro_time_casa.nome, "time": goleiro_time_casa.time}
    timeB = jogador_to_dict(jogadores_visitante)
    goleiroB = {"nome": goleiro_time_visitante.nome, "time":goleiro_time_visitante.time}
    # Converte o dicionário para uma string JSON
    json_message = json.dumps({"message": message1, "timeA": timeA, "timeB": timeB, "goleiroA": goleiroA, "goleiroB": goleiroB })  
    # Espera pelo sinal para enviar a mensagem
    event.wait()  
    # Codifica a string JSON antes de enviar via socket
    server_socket.sendto(json_message.encode(), client_address) 

# Lida com registros de clientes
def handle_client_registration(server_socket, clients, exit_flag):
    # Define um timeout random entre 3 e 9 segundos
    server_socket.settimeout(random.randint(3,9)) 
    while not exit_flag[0]:
        try:
            message, address = server_socket.recvfrom(1024)
        except (socket.timeout, TimeoutError):  # catch both TimeoutError and socket.timeout
            exit_flag[0] = True
        with open("server.log", "a") as f:
            f.write(f"\n(server) Received {message} of address {address} on socket")
            if message.decode() == "register":
                f.write(f"\n(server) Registering client {address}. \n")
                clients.add(address)
            elif message.decode() == "unregister":
                f.write(f"\n(server) Unregistering client {address}. \n")
                clients.discard(address)
            f.write(f"\n(server) Number of clients registered: {len(clients)}\n")
 

# Define tempo de intervalo entre envio de notificações
user_input = input("(server)Insira o tempo entre os envios de notificações: ")
sleepTime = int(user_input)

port = 12345
# Inicialização do socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Escuta em todas as interfaces de rede
server_socket.bind(("0.0.0.0", port))
# Infos do servidor
server_name = socket.gethostname()
server_ip = socket.gethostbyname(server_name)

with open("server.log", "w") as f:
    f.write(f"(server) Server started on port {port}. \n")
    f.write(f"(server)Server name: {server_name}")
    f.write(f"\n(server)Server ip: {server_ip}")

# Simula uma partida
jogo_simulado, total_eventos = simulate_game.simular_partida() 

# Conjunto de clientes
clients = set()

# Contador de pacotes totais enviados
count = 0

# Cria uma lista para armazenar o sinalizador de saída
exit_flag = [False]
# Inicializa nova thread para lidar com registro de clientes
client_registration_thread = threading.Thread(target=handle_client_registration, args=(server_socket,clients, exit_flag))
client_registration_thread.start()
        
while count < total_eventos:
    # Preparação para enviar o mesmo pacote para todos os clientes ao mesmo tempo
    event = threading.Event()
    threads = []
    
    # Para cada cliente registrado para receber mensagens
    for client in clients:
        # Cria thread para enviar a mensagem
        thread = threading.Thread(target=send_events_message_to_client, args=(event, client, server_socket))
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

# Para cada cliente no conjunto envia sinal de que a transmissão foi encerrada
for cAddr in clients:
    server_socket.sendto("End of transmission".encode(), cAddr)
    # Escreve mensagem no arquivo de Log
    with open("server.log", "a") as f:
        f.write(f"\n(server) Sended end of transmission message for client {cAddr}. \n")

# Para terminar a thread de registro de clientes no final da execução do programa
exit_flag[0] = True
# Espera a thread terminar
client_registration_thread.join()
print("(server)Jogo Encerrado, encerrando execução!")  