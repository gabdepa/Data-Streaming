import random

time_casa = "Galáticos"
time_visitante = "The Bests"


# Lista de frases de narradores brasileiros para cada evento
frases_futebol = {
    "Gol!": [
        "Gol! A torcida vai à loucura pelo {time}! {jogador} marcou!",
        "Que beleza! Show de bola! {jogador} fez o gol pelo {time}!",
        "Balança as redes! É gol, meu amigo! {jogador} é o herói do {time}!",
        "Artilheiro não perdoa! A rede estufou! {jogador} marca para o {time}!",
        "Show de categoria! {jogador} de letra!",
    ],
    "Gol Perdido!": [
        "{jogador} perdeu uma chance incrível de marcar para o {time}!",
        "O gol estava aberto, mas {jogador} chutou para fora pelo {time}!",
        "Inacreditável! {jogador} não aproveitou a oportunidade para o {time}!",
    ],
    "Defesa!": [
        "Que defesa espetacular! {goleiro} voou como um gato pelo {time}!",
        "A zaga está impenetrável, como uma muralha pelo {time}!",
        "Defesaça! A torcida aplaude {goleiro} pelo {time}!",
        "Goleiro faz milagre! A bola ia no cantinho, mas {goleiro} salvou o {time}!",
        "Bloqueio perfeito! Não passa nada pelo {time}!",
    ],
    "Drible mágico!": [
        "Ele fez chover no gramado! Drible mágico de {jogador} em {adversario}!",
        "{jogador} passou como uma flecha pelos defensores, driblando {adversario}!",
        "Drible desconcertante de {jogador} em {adversario}! Uma verdadeira obra de arte!",
        "Drible seco de {jogador}! {adversario} ficou plantado!",
        "Com um toque de gênio, {jogador} driblou {adversario}!",
    ],
    "Falta!": [
        "O árbitro marca a falta e exibe o cartão amarelo. Olha a malandragem de {jogador} do {time}!",
        "Falta tática de {jogador} do {time} para segurar o contra-ataque.",
        "A barreira está formada. A bola vai na trave!",
        "{jogador} do {time} leva o cartão amarelo por falta dura em {adversario}.",
        "Momento perigoso! A falta pode definir o jogo pelo {time}!",
    ],
    "Cartão Amarelo!": [
        "Cartão amarelo é mostrado para {jogador} do {time}. Ele precisa tomar cuidado!",
        "O árbitro adverte {jogador} do {time} com o cartão amarelo!",
        "Comportamento antidesportivo resulta em cartão amarelo para {jogador} do {time}!",
        "Mais uma entrada dura e o cartão amarelo sai para {jogador} do {time}!",
        "{jogador} do {time} está pendurado após receber o cartão amarelo!",
    ],
    "Cartão Vermelho!": [
        "Cartão vermelho direto! O juiz não perdoou! {jogador} do {time} é expulso após falta em {adversario}!",
        "Comportamento antidesportivo resulta na expulsão de {jogador} do {time} após falta em {adversario}!",
        "Vai assistir o resto do jogo no chuveiro! {jogador} do {time} está fora após falta em {adversario}!",
        "Não dá para escapar da expulsão após essa falta de {jogador} do {time} em {adversario}!",
        "O juiz não hesitou em mostrar o vermelho para {jogador} do {time} após falta em {adversario}!",
    ],
    "Pênalti!!": [
        "O árbitro aponta para a marca da cal. É pênalti! {jogador} do {time} enfrenta o goleiro!",
        "Cobrador contra goleiro. Quem leva a melhor? {jogador} do {time} está pronto!",
        "Defendeu! Goleiro pegou o pênalti de {jogador} do {time}! Frustração no rosto do artilheiro!",
        "A torcida fica em silêncio enquanto {jogador} do {time} se prepara para a cobrança.",
    ]
}


# Distribuição de probabilidade aproximada para eventos em uma partida de futebol
distribuicao_probabilidade = {
    "Gol!": 0.03,  # Diminuí a probabilidade de gol
    "Gol Perdido!": 0.12,  # Novo evento: jogador perde o gol
    "Defesa!": 0.15,
    "Drible mágico!": 0.2,
    "Falta!": 0.2,
    "Cartão Amarelo!": 0.15,
    "Cartão Vermelho!": 0.05,
    "Pênalti!!": 0.2,  # Aumentei a probabilidade de pênalti
}



class Jogador:
    def __init__(self, nome, time, posicao):
        self.nome = nome
        self.time = time
        self.cartao_vermelho = False  # Adicione um atributo para controlar se o jogador recebeu cartão vermelho
        self.posicao = posicao

class Goleiro:
    def __init__(self, nome, equipe):
        self.nome = nome
        self.equipe = equipe


# Lista de jogadores que não são goleiros
jogadores_casa = [
    Jogador("Roberto Carlos", time_casa, "Lateral Esquerdo"),
    Jogador("Cafu", time_casa, "Lateral Direito"),
    Jogador("Cannavaro", time_casa, "Zagueiro"),
    Jogador("Beckenbauer", time_casa, "Zagueiro"),
    Jogador("Iniesta", time_casa, "Meio-Campo"),
    Jogador("Xavi", time_casa, "Meio-Campo"),
    Jogador("Zidane", time_casa, "Meio-Campo"), 
    Jogador("Ronaldinho", time_casa, "Meio-Campo"), 
    Jogador("Pelé", time_casa, "Atacante"), 
    Jogador("Cruyff", time_casa, "Atacante"), 
]

jogadores_visitante = [
    Jogador("Carlos Alberto", time_visitante, "Lateral Direito"),
    Jogador("Marcelo", time_visitante, "Lateral Esquerdo"),
    Jogador("Maldini", time_visitante, "Zagueiro"),
    Jogador("Sergio Ramos", time_visitante, "Zagueiro"),
    Jogador("Pirlo", time_visitante, "Meio-Campo"),
    Jogador("Seedorf", time_visitante, "Meio-Campo"),
    Jogador("Kaká", time_visitante, "Meio-Campo"),
    Jogador("Messi", time_visitante, "Meio-Campo"),
    Jogador("Neymar", time_visitante, "Atacante"),
    Jogador("Ronaldo", time_visitante, "Atacante"),
]

# Criação dos objetos dos goleiros
goleiro_time_casa = Goleiro("Dida", time_casa)
goleiro_time_visitante = Goleiro("Buffon", time_visitante)

def simular_partida(total_eventos_jogo):
    jogo_simulado = []  # Lista para armazenar o placar, a frase de cada evento e o tempo de jogo

    # Placar inicial
    placar_casa = 0
    placar_visitante = 0
    tempo = 0


    # Lista de jogadores que receberam cartão vermelho
    jogadores_cartao_vermelho = []

    for i in range(0,total_eventos_jogo):
        evento = random.choices(
            list(distribuicao_probabilidade.keys()),
            weights=list(distribuicao_probabilidade.values())
        )[0]

        if evento == "Defesa!":
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
        if evento == "Gol!":
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


        if evento == "Cartão Vermelho!":
            jogador.cartao_vermelho = True  # Marca o jogador com cartão vermelho
            jogadores_cartao_vermelho.append(jogador)

        placar = "Placar: {0} {1} - {2} {3}".format(time_casa,placar_casa, placar_visitante,time_visitante)

        tempo+=1
        if tempo > 45 and tempo < 50:
            tempo_jogo = "Tempo de Jogo: 45+{0}'".format(tempo-45)    
        elif tempo > 90:
            tempo_jogo = "Tempo de Jogo: 90+{0}'".format(tempo-90)
        else:
            tempo_jogo = "Tempo de Jogo: {0}'".format(tempo)
        jogo_simulado.append((placar, frase_evento, evento, tempo_jogo))

    # print(jogo_simulado)
    # print("Placar final: {} - {}".format(placar_casa, placar_visitante))
    return jogo_simulado