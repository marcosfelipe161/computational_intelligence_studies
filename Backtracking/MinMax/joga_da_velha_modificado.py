import pygame
import sys
import time

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

# Inicializar pygame
pygame.init()
tamanho = 600
tela = pygame.display.set_mode((tamanho, tamanho))
pygame.display.set_caption("Jogo da Velha")

# Fonte
fonte = pygame.font.SysFont(None, 150)

# Tabuleiro
tabuleiro = [" " for _ in range(9)]

def desenhar_tabuleiro():
    tela.fill(BRANCO)
    esp = tamanho // 3
    for i in range(1, 3):
        pygame.draw.line(tela, PRETO, (0, i * esp), (tamanho, i * esp), 5)
        pygame.draw.line(tela, PRETO, (i * esp, 0), (i * esp, tamanho), 5)
    
    for i in range(9):
        x = (i % 3) * esp
        y = (i // 3) * esp
        if tabuleiro[i] == "X":
            texto = fonte.render("X", True, AZUL)
            tela.blit(texto, (x + 50, y + 10))
        elif tabuleiro[i] == "O":
            texto = fonte.render("O", True, VERMELHO)
            tela.blit(texto, (x + 50, y + 10))
    
    pygame.display.flip()

def verificar_vencedor(tabuleiro, jogador):
    combinacoes = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for c in combinacoes:
        if all(tabuleiro[i] == jogador for i in c):
            return True
    return False

def verificar_empate(tabuleiro):
    return " " not in tabuleiro

def minimax(tab, profundidade, maximizando):
    if verificar_vencedor(tab, "O"):  # computador
        return 10 - profundidade
    if verificar_vencedor(tab, "X"):  # jogador
        return -10 + profundidade
    if verificar_empate(tab):
        return 0

    if maximizando:
        melhor = -float("inf")
        for i in range(9):
            if tab[i] == " ":
                tab[i] = "O"
                val = minimax(tab, profundidade + 1, False)
                tab[i] = " "
                melhor = max(melhor, val)
        return melhor
    else:
        melhor = float("inf")
        for i in range(9):
            if tab[i] == " ":
                tab[i] = "X"
                val = minimax(tab, profundidade + 1, True)
                tab[i] = " "
                melhor = min(melhor, val)
        return melhor

def melhor_jogada(tab):
    melhor_valor = -float("inf")
    melhor_posicao = -1
    ordem_preferencia = [4, 0, 2, 6, 8, 1, 3, 5, 7]

    for i in ordem_preferencia:
        if tab[i] == " ":
            tab[i] = "O"
            val = minimax(tab, 0, False)
            tab[i] = " "
            if val > melhor_valor:
                melhor_valor = val
                melhor_posicao = i
    return melhor_posicao

def mostrar_mensagem(texto):
    tela.fill(BRANCO)
    msg = pygame.font.SysFont(None, 70).render(texto, True, PRETO)
    tela.blit(msg, (60, tamanho // 2 - 30))
    pygame.display.flip()
    time.sleep(2)

def posicao_do_mouse(x, y):
    linha = y // (tamanho // 3)
    coluna = x // (tamanho // 3)
    return linha * 3 + coluna

# Loop principal
jogando = True
vez_do_jogador = True  # Jogador começa agora

while jogando:
    desenhar_tabuleiro()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN and vez_do_jogador:
            x, y = pygame.mouse.get_pos()
            pos = posicao_do_mouse(x, y)
            if tabuleiro[pos] == " ":
                tabuleiro[pos] = "X"
                vez_do_jogador = False

                if verificar_vencedor(tabuleiro, "X"):
                    desenhar_tabuleiro()
                    mostrar_mensagem("Você venceu!")
                    jogando = False
                elif verificar_empate(tabuleiro):
                    desenhar_tabuleiro()
                    mostrar_mensagem("Empate!")
                    jogando = False

    if not vez_do_jogador and jogando:
        pygame.time.delay(500)
        pos = melhor_jogada(tabuleiro)
        if pos != -1:
            tabuleiro[pos] = "O"
        vez_do_jogador = True

        if verificar_vencedor(tabuleiro, "O"):
            desenhar_tabuleiro()
            mostrar_mensagem("Computador venceu!")
            jogando = False
        elif verificar_empate(tabuleiro):
            desenhar_tabuleiro()
            mostrar_mensagem("Empate!")
            jogando = False
