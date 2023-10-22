import socket
import time
import threading
import json 

port = 12345

# Função para enviar mensagem para um cliente
def send_message_to_client(event, client_address, server_socket):
    print(f"(server) Sending message to client {client_address}")
    message = {"count": count, "content": i}  # Crie um dicionário para a mensagem
    json_message = json.dumps({"message": message})  # Converta o dicionário para uma string JSON
    event.wait()  # Espera pelo sinal para enviar a mensagem
    server_socket.sendto(json_message.encode(), client_address)  # Codifique a string JSON antes de enviar
 

# Inicialização do socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", port))  # Escuta em todas as interfaces de rede
server_socket.setblocking(0)  # Socket não bloqueante
print(f"(server) Server started on port {port}.")

# Conjunto de clientes
clients = set()

# Mensagem
i = 0
# Contador de pacotes totais enviados
count = 0

while True:
    try:
        # Recebe mensagem e endereço do socket
        message, address = server_socket.recvfrom(1024)
        print(f"\n(server) Received {message} of address {address} on socket")

        # Registra o cliente no conjunto de clientes
        if message.decode() == "register":
            print(f"(server) Registering client {address}.")
            clients.add(address)
        elif message.decode() == "unregister":
            print(f"(server) Unregistering client {address}.")
            clients.discard(address)
        print(f"(server) Number of clients registered: {len(clients)}\n")

    except BlockingIOError:
        # Sem dados para ler, então faça outras coisas
        pass

    # Preparação para enviar o mesmo pacote para todos os clientes ao mesmo tempo
    event = threading.Event()
    threads = []
    
    for client in clients:
        thread = threading.Thread(target=send_message_to_client, args=(event, client, server_socket))
        threads.append(thread)
        thread.start()

    # Dispara o sinal para todos os threads enviarem a mensagem
    event.set()  

    for thread in threads:
        thread.join()

    # Intervalo de tempo entre cada mensagem (1 segundo)
    time.sleep(1)  
    i += 1
    count += 1
