import copy

# Retorna X ou O
def jogador(tabuleiro):
    return 'X' if sum(row.count('X') for row in tabuleiro) == sum(row.count('O') for row in tabuleiro) else 'O'

# Retorna todas as jogadas disponíveis
def acoes(tabuleiro):
    return [(i, j) for i in range(3) for j in range(3) if tabuleiro[i][j] == ' ']

# Retorna o tabuleiro que resulta ao fazer uma jogada do vetor de ações
def resultado(tabuleiro, acao):
    novo_tabuleiro = copy.deepcopy(tabuleiro)
    novo_tabuleiro[acao[0]][acao[1]] = jogador(tabuleiro)
    return novo_tabuleiro

# Retorna o ganhador, se houver
def ganhador(tabuleiro):
    linhas = tabuleiro + [[tabuleiro[j][i] for j in range(3)] for i in range(3)] + \
             [[tabuleiro[i][i] for i in range(3)]] + \
             [[tabuleiro[i][2 - i] for i in range(3)]]
    for linha in linhas:
        if linha.count('X') == 3:
            return 'X'
        elif linha.count('O') == 3:
            return 'O'
    return None

# Retorna Verdadeiro se o jogo acabou, Falso caso contrário
def final(tabuleiro):
    return ganhador(tabuleiro) or all(' ' not in row for row in tabuleiro)

# Retorna 1 se X ganhou, -1 se O ganhou, 0 caso contrário.
def custo(tabuleiro):
    vencedor = ganhador(tabuleiro)
    if vencedor == 'X':
        return 1
    elif vencedor == 'O':
        return -1
    else:
        return 0

# Retorna a jogada ótima para o jogador atual
def minimax(tabuleiro):
    if jogador(tabuleiro) == 'X':
        return maxValor(tabuleiro)[1]
    else:
        return minValor(tabuleiro)[1]

def maxValor(tabuleiro):
    if final(tabuleiro):
        return custo(tabuleiro), None

    max_utilidade = float('-inf')
    melhor_acao = None

    for acao in acoes(tabuleiro):
        novo_estado = resultado(tabuleiro, acao)
        utilidade, _ = minValor(novo_estado)
        if utilidade > max_utilidade:
            max_utilidade = utilidade
            melhor_acao = acao

    return max_utilidade, melhor_acao

def minValor(tabuleiro):
    if final(tabuleiro):
        return custo(tabuleiro), None

    min_utilidade = float('inf')
    melhor_acao = None

    for acao in acoes(tabuleiro):
        novo_estado = resultado(tabuleiro, acao)
        utilidade, _ = maxValor(novo_estado)
        if utilidade < min_utilidade:
            min_utilidade = utilidade
            melhor_acao = acao

    return min_utilidade, melhor_acao

# Função para imprimir o tabuleiro
def imprimir_tabuleiro(tabuleiro):
    for row in tabuleiro:
        print('|'.join(row))
        print('-' * 5)

# Função para o jogador humano fazer uma jogada
def jogador_humano(tabuleiro):
    while True:
        try:
            linha = int(input("Digite a linha (0, 1, ou 2): "))
            coluna = int(input("Digite a coluna (0, 1, ou 2): "))
            if tabuleiro[linha][coluna] == ' ':
                return linha, coluna
            else:
                print("Essa posição já foi preenchida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Tente novamente.")

# Função principal do jogo
def jogar_jogo_da_velha():
    tabuleiro = [[' ']*3 for _ in range(3)]
    while not final(tabuleiro):
        imprimir_tabuleiro(tabuleiro)
        if jogador(tabuleiro) == 'X':
            linha, coluna = jogador_humano(tabuleiro)
            tabuleiro[linha][coluna] = 'X'
        else:
            print("Computador está pensando...")
            linha, coluna = minimax(tabuleiro)
            tabuleiro[linha][coluna] = 'O'
    imprimir_tabuleiro(tabuleiro)
    vencedor = ganhador(tabuleiro)
    if vencedor:
        print(f"O vencedor é o jogador {vencedor}. Parabéns!")
    else:
        print("Empate!")

# Iniciar o jogo
jogar_jogo_da_velha()
