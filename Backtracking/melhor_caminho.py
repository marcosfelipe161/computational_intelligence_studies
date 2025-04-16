# Dado um tabuleiro NXN, marque o melhor caminho encontrado 
# entre uma posição inicial e uma posição final. A definição 
# do tabuleiro será feito em uma matriz que vai conter espaços 
# vazios e espaços bloqueados (utilize um X).

# Função para exibir o tabuleiro no terminal
# a funcao destaca a posição atual com um asterisco vermelho 
# e marca os caminhos já percorridos com um pnto

def mostrar_tabuleiro(tabuleiro, pos_atual=None, rastro=None):
    rastro = rastro or set()
    for i, linha in enumerate(tabuleiro):
        linha_formatada = []
        for j, celula in enumerate(linha):
            if (i, j) == pos_atual:
                linha_formatada.append(f"\033[1;31m*\033[0m")  # Posição atual em vermelho
            elif (i, j) in rastro:
                linha_formatada.append("·")                    # Caminho já percorrido
            else:
                linha_formatada.append(celula)
        print("|" + "|".join(linha_formatada) + "|")

# Função que encontra o melhor caminho entre o ponto inicial e o destino
# Usa BFS para encontrar o caminho mais curto
def encontrar_melhor_caminho(tabuleiro, inicio, destino, n):
    from collections import deque

    tab_copia = [linha[:] for linha in tabuleiro]  # copia da matriz original
    fila = deque([(inicio[0], inicio[1], [])])     # Fila para BFS, armazena (linha, coluna, caminho até aqui)
    visitados = set([(inicio[0], inicio[1])])      # Conjunto de posições já visitadas
    direcoes = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Direções possíveis: direita, esquerda, baixo, cima

    rastro_da_busca = []  # Para armazenar o rastro completo da busca

    while fila:
        linha, coluna, caminho = fila.popleft()  # Pega próxima posição da fila
        rastro_da_busca.append((linha, coluna, caminho))  # Salva o passo atual

        if (linha, coluna) == destino:
            return caminho + [(linha, coluna)], rastro_da_busca  # Caminho encontrado!

        for dl, dc in direcoes:
            nl, nc = linha + dl, coluna + dc  # Nova linha e nova coluna
            # Verifica se a nova posição está dentro do tabuleiro e é válida
            if 0 <= nl < n and 0 <= nc < n:
                if (tab_copia[nl][nc] == ' ' or (nl, nc) == destino) and (nl, nc) not in visitados:
                    visitados.add((nl, nc))  # Marca como visitado
                    fila.append((nl, nc, caminho + [(linha, coluna)]))  # Adiciona na fila para continuar a busca

    return None, rastro_da_busca  # Nenhum caminho foi encontrado

# Mostra o passo a passo da busca de forma interativa no terminal
# Útil quando não se encontra o caminho, para entender o processo
def mostrar_passos_interativamente(tabuleiro, passos):
    for i, (linha, coluna, caminho) in enumerate(passos):
        print(f"\nPasso {i + 1}: Analisando posição ({linha}, {coluna})")
        rastro = set(caminho)
        mostrar_tabuleiro(tabuleiro, (linha, coluna), rastro)
        input("Pressione Enter para continuar...")  # Aguarda usuário para continuar

# Exibe o caminho final encontrado
def mostrar_caminho_final(tabuleiro, caminho):
    for i, pos in enumerate(caminho):
        print(f"\nPasso {i + 1}/{len(caminho)}: posição {pos}")
        rastro = set(caminho[:i])
        mostrar_tabuleiro(tabuleiro, pos, rastro)
        input("Pressione Enter para continuar...")

# Função principal que define o tabuleiro, os pontos de partida e destino
# executa a busca e mostra o resultado final
def main():
    tabuleiro = [
        [' ', 'X', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', 'X', ' ', ' '],
        [' ', 'X', ' ', ' ']
    ]
    n = len(tabuleiro)
    inicio = (3, 0)      # Posição inicial
    destino = (0, 3)     # Posição final

    print("Tabuleiro Inicial:")
    mostrar_tabuleiro(tabuleiro, inicio)

    # Executa a busca pelo melhor caminho
    caminho, rastro_da_busca = encontrar_melhor_caminho(tabuleiro, inicio, destino, n)

    if caminho:
        print("\n\033[1;32mCaminho encontrado!\033[0m")
        mostrar_caminho_final(tabuleiro, caminho)

        # Exibe o caminho final com numeração em ordem
        print("\n\033[1;34mCaminho final numerado:\033[0m")
        tab_final = [linha[:] for linha in tabuleiro]
        for passo, (l, c) in enumerate(caminho):
            # Substitui a posição no tabuleiro pelo número do passo
            tab_final[l][c] = str(passo + 1) if passo < 9 else chr(ord('a') + passo - 9)
        mostrar_tabuleiro(tab_final)
    else:
        print("\n\033[1;31mNão há caminho possível!\033[0m")
        mostrar_passos_interativamente(tabuleiro, rastro_da_busca)

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
