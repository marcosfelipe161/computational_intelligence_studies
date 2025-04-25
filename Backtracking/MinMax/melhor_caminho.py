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


# Distância absoluta entre pontos
def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Função que encontra o melhor caminho entre o ponto inicial e o destino
# Usa BFS para encontrar o caminho mais curto
def melhor_caminho(tabuleiro, destino, fila, visitados, rastro_da_busca, melhor_falha):
    if not fila:
        return None, rastro_da_busca, melhor_falha

    linha, coluna, caminho = fila[0]
    rastro_da_busca.append((linha, coluna, caminho))

    # Atualiza a melhor tentativa com base na distância ao destino
    dist = distancia((linha, coluna), destino)
    if dist < melhor_falha["dist"]:
        melhor_falha["pos"] = (linha, coluna)
        melhor_falha["caminho"] = caminho + [(linha, coluna)]
        melhor_falha["dist"] = dist

    if (linha, coluna) == destino:
        return caminho + [(linha, coluna)], rastro_da_busca, melhor_falha

    n = len(tabuleiro)
    direcoes = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    novos_passos = []

    for dl, dc in direcoes:
        nl, nc = linha + dl, coluna + dc
        if 0 <= nl < n and 0 <= nc < n:
            if (tabuleiro[nl][nc] == ' ' or (nl, nc) == destino) and (nl, nc) not in visitados:
                visitados.add((nl, nc))
                novos_passos.append((nl, nc, caminho + [(linha, coluna)]))

    return melhor_caminho(tabuleiro, destino, fila[1:] + novos_passos, visitados, rastro_da_busca, melhor_falha)


# Mostra passo a passo da tentativa
def mostrar_passos(tabuleiro, passos):
    for i, (linha, coluna, caminho) in enumerate(passos):
        print(f"\nPasso {i + 1}: Analisando posição ({linha}, {coluna})")
        rastro = set(caminho)
        mostrar_tabuleiro(tabuleiro, (linha, coluna), rastro)
        input("Pressione Enter para continuar...")

def mostrar_caminho_final(tabuleiro, caminho):
    for i, pos in enumerate(caminho):
        print(f"\nPasso {i + 1}/{len(caminho)}: posição {pos}")
        rastro = set(caminho[:i])
        mostrar_tabuleiro(tabuleiro, pos, rastro)
        input("Pressione Enter para continuar...")


# Função principal
def main():
    tabuleiro = [
        [' ', 'X', 'X', ' '],
        [' ', ' ', ' ', ' '],
        [' ', 'X', ' ', ' '],
        [' ', 'X', ' ', ' ']
    ]
    inicio = (3, 0)
    destino = (0, 3)

    print("Tabuleiro Inicial:")
    mostrar_tabuleiro(tabuleiro, inicio)

    visitados = set([inicio])
    fila = [(inicio[0], inicio[1], [])]
    rastro_da_busca = []
    melhor_falha = {
        "pos": inicio,
        "caminho": [],
        "dist": float('inf')
    }

    caminho, rastro, melhor_falha = melhor_caminho(tabuleiro, destino, fila, visitados, rastro_da_busca, melhor_falha)

    if caminho:
        print("\n\033[1;32mCaminho encontrado!\033[0m")
        mostrar_caminho_final(tabuleiro, caminho)

        print("\n\033[1;34mCaminho final:\033[0m")
        tab_final = [linha[:] for linha in tabuleiro]
        for passo, (l, c) in enumerate(caminho):
            tab_final[l][c] = str(passo + 1) if passo < 9 else chr(ord('a') + passo - 9)
        mostrar_tabuleiro(tab_final)
    else:
        print("\n\033[1;31mNão há caminho possível!\033[0m")
        mostrar_caminho_final(tabuleiro, melhor_falha["caminho"])
        print(f"\n\033[1;33mDistância mínima até o destino: {melhor_falha['dist']}\033[0m")


if __name__ == "__main__":
    main()
