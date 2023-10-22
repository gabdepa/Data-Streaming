import socket
import time
import threading

# Função para enviar mensagem para um cliente
def send_message_to_client(event, client_address, message, server_socket):
    event.wait()  # Espera pelo sinal para enviar a mensagem
    server_socket.sendto(message.encode(), client_address)

# Inicialize o socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 12345))  # Escuta em todas as interfaces de rede
server_socket.setblocking(0)  # Socket não bloqueante

clients = set()

i = 0
while True:
    try:
        # Recebe mensagem e endereço do socket
        message, address = server_socket.recvfrom(1024)
        print(f"(server) Receive a message and address on socket => {message}, {address}")

        # Registra o cliente no conjunto de clientes
        if message.decode() == "register":
            clients.add(address)
        elif message.decode() == "unregister":
            clients.discard(address)

    except BlockingIOError:
        # Sem dados para ler, então faça outras coisas
        pass

    # Preparação para enviar o mesmo pacote para todos os clientes ao mesmo tempo
    event = threading.Event()
    threads = []
    for client in clients:
        thread = threading.Thread(target=send_message_to_client, args=(event, client, f"Message {i}", server_socket))
        threads.append(thread)
        thread.start()

    event.set()  # Dispara o sinal para todos os threads enviarem a mensagem

    for thread in threads:
        thread.join()

    time.sleep(1)  # Intervalo de tempo entre cada mensagem (1 segundo)
    i += 1
