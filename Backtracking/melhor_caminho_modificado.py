import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from collections import deque

# Gera um tabuleiro 3x10 com obstáculos aleatórios e define ponto inicial e final
def gerar_tabuleiro():
    linhas, colunas = 3, 10
    tabuleiro = [[' ' for _ in range(colunas)] for _ in range(linhas)]  # Cria tabuleiro vazio

    obstaculos = set()
    while len(obstaculos) < 6:                      # Define a quantidade de obstaculos
        i = random.randint(0, linhas - 1)
        j = random.randint(0, colunas - 1)

        if (i, j) not in [(0, 0), (linhas-1, colunas-1)]:
            obstaculos.add((i, j))

    # Marca os obstáculos no tabuleiro
    for i, j in obstaculos:
        tabuleiro[i][j] = 'X'

    inicio = (0, 0)
    destino = (0, 9)
    return tabuleiro, inicio, destino

# Calcula a distância entre dois pontos (heurística simples)
def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Busca o caminho mais curto entre início e destino usando BFS 
def encontrar_melhor_caminho(tabuleiro, inicio, destino):
    linhas, colunas = len(tabuleiro), len(tabuleiro[0])
    fila = deque([(inicio[0], inicio[1], [])])  # Fila armazena posição atual + caminho percorrido
    visitados = set([inicio])                  # Evita visitar posições repetidas
    direcoes = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Direções possíveis: direita, esquerda, baixo, cima

    melhores_tentativas = []  # Guarda caminhos incompletos, caso nenhum completo seja possível

    while fila:
        linha, coluna, caminho = fila.popleft()

        if (linha, coluna) == destino:
            return caminho + [(linha, coluna)], None  # Caminho válido encontrado

        movimentos_possiveis = 0  # Contador para detectar becos sem saída
        for dl, dc in direcoes:
            nl, nc = linha + dl, coluna + dc
            if 0 <= nl < linhas and 0 <= nc < colunas:
                if (tabuleiro[nl][nc] != 'X') and ((nl, nc) not in visitados):
                    visitados.add((nl, nc))
                    fila.append((nl, nc, caminho + [(linha, coluna)]))
                    movimentos_possiveis += 1

        # Se não houverem mais movimentos, registra o caminho como tentativa falha
        if movimentos_possiveis == 0:
            tentativa_falha = caminho + [(linha, coluna)]
            melhores_tentativas.append(tentativa_falha)

    # Caso não encontre caminho, retorna a tentativa mais próxima do destino
    if melhores_tentativas:
        melhor = min(melhores_tentativas, key=lambda t: distancia(t[-1], destino))
        return None, melhor
    else:
        return None, [inicio]

# Cria matriz numérica para visualização com matplotlib:
# 0 = vazio, 1 = obstáculo, 2 = caminho, 3 = posição atual
def criar_matriz_visual(tabuleiro, pos_atual=None, rastro=None):
    linhas, colunas = len(tabuleiro), len(tabuleiro[0])
    matriz = np.zeros((linhas, colunas))
    for i in range(linhas):
        for j in range(colunas):
            if tabuleiro[i][j] == 'X':
                matriz[i][j] = 1
    if rastro:
        for i, j in rastro:
            matriz[i][j] = 2
    if pos_atual:
        i, j = pos_atual
        matriz[i][j] = 3
    return matriz

# Gera uma animação visual da busca no matplotlib
def animar_busca(tabuleiro, passos, caminho_encontrado=True):
    fig, ax = plt.subplots()
    mat = criar_matriz_visual(tabuleiro)  # Matriz inicial
    img = ax.imshow(mat, cmap='viridis', vmin=0, vmax=3)  # Configuração de cor e escala

    # Mensagem de sucesso ou fracasso
    mensagem = "Caminho encontrado!" if caminho_encontrado else "Não há caminho possível!"
    cor_texto = 'green' if caminho_encontrado else 'red'
    ax.text(0.5, 1.35, mensagem, color=cor_texto, fontsize=16, ha='center', va='center', transform=ax.transAxes)

    # Função chamada a cada frame da animação
    def atualizar(frame):
        l, c, caminho = passos[frame]
        nova_matriz = criar_matriz_visual(tabuleiro, (l, c), set(caminho))  # Atualiza matriz visual
        img.set_data(nova_matriz)
        ax.set_title(f"Passo {frame + 1}/{len(passos)}")
        return [img]

    ani = animation.FuncAnimation(fig, atualizar, frames=len(passos), interval=500, repeat=False)
    return ani

# Função principal: gera o tabuleiro, executa a busca e exibe o resultado visualmente
def main():
    random.seed()
    tabuleiro, inicio, destino = gerar_tabuleiro()
    caminho, tentativa = encontrar_melhor_caminho(tabuleiro, inicio, destino)

    if caminho:
        print("\033[1;32mCaminho encontrado!\033[0m")
        # Prepara os passos para animação do caminho encontrado
        anim_steps = [(l, c, caminho[:i]) for i, (l, c) in enumerate(caminho)]
        ani = animar_busca(tabuleiro, anim_steps, caminho_encontrado=True)
    else:
        print("\033[1;31mNão há caminho possível!\033[0m")
        # Anima a tentativa mais próxima do destino
        anim_steps = [(l, c, tentativa[:i]) for i, (l, c) in enumerate(tentativa)]
        ani = animar_busca(tabuleiro, anim_steps, caminho_encontrado=False)

    plt.show()  
if __name__ == "__main__":
    main()
