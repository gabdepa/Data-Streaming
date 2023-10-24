import socket
import time
import threading
import json 
import random

port = 12345
import random

class Jogador:
    def __init__(self, nome, time):
        self.nome = nome
        self.time = time
        self.cartao_vermelho = False  # Adicione um atributo para controlar se o jogador recebeu cartão vermelho

class Goleiro:
    def __init__(self, nome, equipe):
        self.nome = nome
        self.equipe = equipe

time_casa = "Time A"
time_visitante = "Time B"

# Lista de frases de narradores brasileiros para cada evento
frases_futebol = {
    "gol": [
        "Gol! É tetra! A torcida vai à loucura pelo {time}! {jogador} marcou!",
        "Que beleza! Show de bola! {jogador} fez o gol pelo {time}!",
        "Balança as redes! É gol, meu amigo! {jogador} é o herói do {time}!",
        "Artilheiro não perdoa! A rede estufou! {jogador} marca para o {time}!",
        "Show de categoria! É o primeiro gol para o {time}! {jogador} é o responsável!",
    ],
    "perdeu_o_gol": [
        "{jogador} perdeu uma chance incrível de marcar para o {time}!",
        "O gol estava aberto, mas {jogador} chutou para fora pelo {time}!",
        "Inacreditável! {jogador} não aproveitou a oportunidade para o {time}!",
    ],
    "defesa": [
        "Que defesa espetacular! {goleiro} voou como um gato pelo {time}!",
        "A zaga está impenetrável, como uma muralha pelo {time}!",
        "Defesaça! A torcida aplaude {goleiro} pelo {time}!",
        "Goleiro faz milagre! A bola ia no cantinho, mas {goleiro} salvou o {time}!",
        "Bloqueio perfeito! Não passa nada pelo {time}!",
    ],
    "drible": [
        "Ele fez chover no gramado! Drible mágico de {jogador} em {adversario}!",
        "{jogador} passou como uma flecha pelos defensores, driblando {adversario}!",
        "Drible desconcertante de {jogador} em {adversario}! Uma verdadeira obra de arte!",
        "Drible seco de {jogador}! {adversario} ficou plantado!",
        "Com um toque de gênio, {jogador} driblou {adversario}!",
    ],
    "falta": [
        "O árbitro marca a falta e exibe o cartão amarelo. Olha a malandragem de {jogador} do {time}!",
        "Falta tática de {jogador} do {time} para segurar o contra-ataque.",
        "A barreira está formada. A bola vai no ângulo!",
        "{jogador} do {time} leva o cartão amarelo por falta dura em {adversario}.",
        "Momento perigoso! A falta pode definir o jogo pelo {time}!",
    ],
    "cartão_amarelo": [
        "Cartão amarelo é mostrado para {jogador} do {time}. Ele precisa tomar cuidado!",
        "O árbitro adverte {jogador} do {time} com o cartão amarelo!",
        "Comportamento antidesportivo resulta em cartão amarelo para {jogador} do {time}!",
        "Mais uma entrada dura e o cartão amarelo sai para {jogador} do {time}!",
        "{jogador} do {time} está pendurado após receber o cartão amarelo!",
    ],
    "cartão_vermelho": [
        "Cartão vermelho direto! O juiz não perdoou! {jogador} do {time} é expulso após falta em {adversario}!",
        "Comportamento antidesportivo resultina na expulsão de {jogador} do {time} após falta em {adversario}!",
        "Vai assistir o resto do jogo no chuveiro! {jogador} do {time} está fora após falta em {adversario}!",
        "Não dá para escapar da expulsão após essa falta de {jogador} do {time} em {adversario}!",
        "O juiz não hesitou em mostrar o vermelho para {jogador} do {time} após falta em {adversario}!",
    ],
    "pênalti": [
        "O árbitro aponta para a marca da cal. É pênalti! {jogador} do {time} enfrenta o goleiro!",
        "Cobrador contra goleiro. Quem leva a melhor? {jogador} do {time} está pronto!",
        "Defendeu! Goleiro pegou o pênalti de {jogador} do {time}! Frustração no rosto do artilheiro!",
        "Cobrança perfeita! Bola na rede! {jogador} do {time} é o artilheiro!",
        "A torcida fica em silêncio enquanto {jogador} do {time} se prepara para a cobrança.",
    ]
}


# Distribuição de probabilidade aproximada para eventos em uma partida de futebol
distribuicao_probabilidade = {
    "gol": 0.03,  # Diminuí a probabilidade de gol
    "perdeu_o_gol": 0.12,  # Novo evento: jogador perde o gol
    "defesa": 0.15,
    "drible": 0.2,
    "falta": 0.2,
    "cartão_amarelo": 0.15,
    "cartão_vermelho": 0.05,
    "pênalti": 0.2,  # Aumentei a probabilidade de pênalti
}
jogo_simulado = []  # Lista para armazenar o placar e a frase de cada evento

def simular_partida():


    # Lista de jogadores que não são goleiros
    jogadores_casa = [Jogador("Neymar", time_casa), Jogador("Messi", time_casa), Jogador("Ronaldo", time_casa), Jogador("Maradona", time_casa), Jogador("Zico", time_casa)]
    jogadores_visitante = [Jogador("Pelé", time_visitante), Jogador("Beckenbauer", time_visitante), Jogador("Cruyff", time_visitante), Jogador("Ronaldinho", time_visitante), Jogador("Iniesta", time_visitante)]

    # Criação dos objetos dos goleiros
    goleiro_time_casa = Goleiro("Taffarel", time_casa)
    goleiro_time_visitante = Goleiro("Gilberto Silva", time_visitante)

    # Placar inicial
    placar_casa = 0
    placar_visitante = 0

    # Lista de jogadores que receberam cartão vermelho
    jogadores_cartao_vermelho = []


    for i in range(1,100):
        evento = random.choices(
            list(distribuicao_probabilidade.keys()),
            weights=list(distribuicao_probabilidade.values())
        )[0]

        if evento == "defesa":
            # Seleciona um goleiro de cada time para eventos de defesa
            if random.random() < 0.5:
                jogador = random.choice(jogadores_casa)
                goleiro = goleiro_time_casa
            else:
                jogador = random.choice(jogadores_visitante)
                goleiro = goleiro_time_visitante
        else:
            # Seleciona aleatoriamente um jogador de qualquer posição para outros eventos
            jogadores_disponiveis = [j for j in (jogadores_casa + jogadores_visitante) if j not in jogadores_cartao_vermelho]
            if not jogadores_disponiveis:
                break  # Todos os jogadores receberam cartão vermelho
            jogador = random.choice(jogadores_disponiveis)
            goleiro = None

        frase_evento = random.choice(frases_futebol[evento])


        # Atualiza o placar se o evento for um gol
        if evento == "gol":
            if jogador.time == time_casa:
                placar_casa += 1
            else:
                placar_visitante += 1

        # Cria a frase do evento

        dados_format = {
            "adversario": "",  # Inicialmente vazio
            "jogador": "",     # Inicialmente vazio
            "goleiro": "",     # Inicialmente vazio
            "time": "",        # Inicialmente vazio
        }

        if "{adversario}" in frase_evento:
            adversario = random.choice([j for j in (jogadores_casa + jogadores_visitante) if j != jogador])
            dados_format["adversario"] = adversario.nome
        if "{jogador}" in frase_evento:
            dados_format["jogador"] = jogador.nome
        if "{goleiro}" in frase_evento:
            dados_format["goleiro"] = goleiro.nome
        if "{time}" in frase_evento:
            dados_format["time"] = jogador.time

        # Formate a string usando .format com o dicionário
        frase_evento = frase_evento.format(**dados_format)


        if evento == "cartão_vermelho":
            jogador.cartao_vermelho = True  # Marca o jogador com cartão vermelho
            jogadores_cartao_vermelho.append(jogador)


        placar = "Placar: {0} {1} - {2} {3}".format(time_casa,placar_casa, placar_visitante,time_visitante)

        jogo_simulado.append((placar, frase_evento, evento))

    # print(jogo_simulado)
    # print("Placar final: {} - {}".format(placar_casa, placar_visitante))

# Simula uma partida
simular_partida()



# Enviar mensagem para um cliente
def send_message_to_client(event, client_address, server_socket):
    print(f"(server) Sending message to client {client_address}")
    # Cria um dicionário para a mensagem
    message = {"count": count, "score": jogo_simulado[count][0],"content": jogo_simulado[count][1], "type": jogo_simulado[count][2]} # added type to datagram, which is the type of the event of the stream   
    # Converte o dicionário para uma string JSON
    json_message = json.dumps({"message": message })  
    # Espera pelo sinal para enviar a mensagem
    event.wait()  
    # Codifica a string JSON antes de enviar via socket
    server_socket.sendto(json_message.encode(), client_address)  
 
user_input = input("Insira o tempo entre os envios de notificações")
sleepTime = int(user_input)
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
        # Retira cliente do conjunto de clientes
        elif message.decode() == "unregister":
            print(f"(server) Unregistering client {address}.")
            clients.discard(address)
        # Dados de estatística 
        print(f"(server) Number of clients registered: {len(clients)}\n")

    except BlockingIOError:
        # Sem dados para ler continua enviando dados
        pass

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

    # Dispara o sinal para todos as threads enviarem a mensagem
    event.set()  

    # Garante que todas as mensagens sejam enviadas antes que o loop continue
    for thread in threads:
        thread.join()

    # Intervalo de tempo entre cada mensagem 
    time.sleep(sleepTime)  
    i += 1
    count += 1
