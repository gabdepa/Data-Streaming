import socket
import json

# Gera estatísticas
def generateClientStats(receivedEndOfTransmission):
    with open("client_stats.log", "w") as f:
        if receivedEndOfTransmission:
            f.write("\n(client) Received end of transmission.")
        else : 
            f.write("\n(client) Ctrl+C received. Unregistering client.")

        # Dados de estatística de streaming
        f.write(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> STATISTICS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<< \n")
        f.write(f"(client) Number of packets received: {received_packets} \n")
        f.write(f"(client) Number of lost packets: {lost_packets} \n")
        f.write(f"(client) Number of packets out of order: {out_of_order}\n")

# Formata output da escalação dos times
def format_teams(team_a, goleiro_a, team_b, goleiro_b, tempo):
    """
    Format the given team A and team B data into a human-readable string.
    
    Parameters:
    - team_a (list): List of dictionaries containing player data for team A
    - team_b (list): List of dictionaries containing player data for team B
    
    Returns:
    - str: Formatted string
    """
    output = goleiro_a['time'].ljust(45) + goleiro_b['time']+"\n"
    output += "--------".ljust(45) + "--------\n"
    output += goleiro_a['nome'].ljust(45) + goleiro_b['nome']+"\n"
    
    for a, b in zip(team_a, team_b):     
        a_name = f"{a['nome']} {a['posicao']} " 
        
        for tempo_gol in a['tempo_gols']:
            if int(tempo_gol) <= int(tempo): 
                a_name+= '*'

        if a['cartao_vermelho'] and int(a['tempo_cv']) < int(tempo):     
            a_name += " (Red Card)"
        
        
        b_name = f"{b['nome']} {b['posicao']} "
        
        for tempo_gol in b['tempo_gols']:
            if int(tempo_gol) <= int(tempo): 
                b_name+= '*'
        if b['cartao_vermelho'] and int(b['tempo_cv']) < int(tempo) :
            b_name += " (Red Card)"
        
        output += f"{a_name}".ljust(45) + f"{b_name}\n"
        
    return output


# server_address = "127.0.0.1"
server_address = str(input("Enter the server address:"))
port = 12345

# Inicialização do socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Envia solicitação de registro no servidor
client_socket.sendto("register".encode(), (server_address, port))
# Escreve mensagem de conectado ao servidor
with open("client.log", "w") as f:
    f.write(f"(client) Client connected to server {server_address} on port {port}.\n")

lost_packets = 0 # Número de pacotes perdidos
out_of_order = 0 # Número de pacotes fora de ordem
last_received = 0 # Número do último pacote recebido
received_packets = 0  # Contador de pacotes recebidos
first_packet_received = True  # Flag para verificar se é o primeiro pacote recebido

try:
    while True:
        # Recebe mensagem e endereço do socket
        message, address = client_socket.recvfrom(4096)
        
        # Caso recebeu fim da Transmissão
        if message.decode() == "End of transmission":
            # Imprime mensagem de fim de jogo
            print('*'*80)
            print('Fim de jogo!')
            print('*'*80)
            # Gera estatísticas da Transmissão
            generateClientStats(True)
            # Interrompe execução
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
        
        # Atualiza o último pacote recebido
        last_received = current_order

        # Escreve mensagem no arquivo de log
        with open("client.log", "a") as f:
            f.write(f"(client) Received message: {message_dict} from {address} \n") 
        
        # Implementar alguma operação nos dados recebidos......imprime na tela
        print("\n")
        print('*'*80)
        formatted_output = format_teams(message_dict['timeA'], message_dict['goleiroA'], message_dict['timeB'], message_dict['goleiroB'],message_dict['message']['time_passed'])
        print(formatted_output)
        print(message_dict['message']['content'])
        print(message_dict['message']['type'])
        print(message_dict['message']['score'])
        tempo = message_dict['message']['time_passed']

        if tempo > 45 and tempo < 50:
            tempo_jogo = "Tempo de Jogo: 45+{0}'".format(tempo-45)    
        elif tempo > 90:
            tempo_jogo = "Tempo de Jogo: 90+{0}'".format(tempo-90)
        else:
            tempo_jogo = "Tempo de Jogo: {0}'".format(tempo)
        print(tempo_jogo)
        print('*'*80)

# Caso cliente seja interrompido
except KeyboardInterrupt:
    # Envia mensagem de cancelamento de registro ao servidor
    client_socket.sendto("unregister".encode(), (server_address, port))
    # Finaliza estatísticas
    generateClientStats(False)

