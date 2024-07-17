import copy

def jogador(tabuleiro):
    return 'X' if sum(row.count('X') for row in tabuleiro) == sum(row.count('O') for row in tabuleiro) else 'O'

def acoes(tabuleiro):
    return [(i, j) for i in range(3) for j in range(3) if tabuleiro[i][j] == ' ']

def resultado(tabuleiro, acao):
    novo_tabuleiro = copy.deepcopy(tabuleiro)
    novo_tabuleiro[acao[0]][acao[1]] = jogador(tabuleiro)
    return novo_tabuleiro


def custo(tabuleiro):
    vencedor = ganhador_diagonal(tabuleiro)
    if vencedor == 'X':
        return 1
    elif vencedor == 'O':
        return -1
    else:
        return 0

def minimax(tabuleiro):
    if jogador(tabuleiro) == 'X':
        return maxValor(tabuleiro)[1]
    else:
        return minValor(tabuleiro)[1]

def maxValor(tabuleiro):
    if final_diagonal(tabuleiro):
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
    if final_diagonal(tabuleiro):
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

def imprimir_tabuleiro(tabuleiro):
    for row in tabuleiro:
        print('|'.join(row))
        print('-' * 5)

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

def jogar_jogo_da_velha():
    tabuleiro = [[' ']*3 for _ in range(3)]
    while not final_diagonal(tabuleiro):
        imprimir_tabuleiro(tabuleiro)
        if jogador(tabuleiro) == 'X':
            linha, coluna = jogador_humano(tabuleiro)
            tabuleiro[linha][coluna] = 'X'
        else:
            print("Computador está pensando...")
            linha, coluna = minimax(tabuleiro)
            tabuleiro[linha][coluna] = 'O'
    imprimir_tabuleiro(tabuleiro)
    vencedor = ganhador_diagonal(tabuleiro)
    if vencedor:
        print(f"O vencedor é o jogador {vencedor}. Parabéns!")
    else:
        print("Empate!")


#As funções a abaixo foram adicionadas ou modificadas, as acima estão iguais ao codigo do exercício 4.1

# Verifica se há vitória na diagonal
def verificar_diagonal(tabuleiro):

    diagonal_principal = [tabuleiro[i][i] for i in range(3)]
    diagonal_secundaria = [tabuleiro[i][2 - i] for i in range(3)]

    if all(cell == 'X' for cell in diagonal_principal) or all(cell == 'O' for cell in diagonal_principal):
        return diagonal_principal[0]
    elif all(cell == 'X' for cell in diagonal_secundaria) or all(cell == 'O' for cell in diagonal_secundaria):
        return diagonal_secundaria[0]
    return None


# Retorna o ganhador apenas na diagonal
def ganhador_diagonal(tabuleiro):
    diagonal = verificar_diagonal(tabuleiro)
    if diagonal:
        return diagonal
    return None

# Função para verificar se o jogo acabou apenas na diagonal
def final_diagonal(tabuleiro):
    return ganhador_diagonal(tabuleiro) is not None or all(' ' not in row for row in tabuleiro)


# Iniciar o jogo
jogar_jogo_da_velha()


''' 
   Explicação das novas regras.
    Apenas é possivel que um jogador ganhe se conseguir completar a sequência de movimentos na diagonal principal
    ou diagonal secundária do tabuleiro. Mesmo se a seqência for concluída na horizontal ou vertical o jogo
    não será encerrado.

'''


#Sequência de jogadas do jogador que terminarão em empate:
#  (1,1) -> (2,2) -> (2,1) -> (2,0) -> (1,2) -> ()

#Sequência de jogadas do jogador que terminarão em vitória pelo computador:
#  (0,1) -> (1,0) -> (1,2) -> (2,0)