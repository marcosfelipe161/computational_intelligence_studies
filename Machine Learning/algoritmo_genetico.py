# Modelo de regressão linear: salario_previsto = a*experiencia + b*estudo + c



import pandas as pd
import matplotlib.pyplot as plt
import random

def criar_individuo():
    return [random.uniform(0,25000) for _ in range(3)] # não precisa de numero negativos porque o salario só sobe

def criar_populacao():
    return [criar_individuo() for _ in range(100)]

def ler_csv():
    df = pd.read_csv("/home/felipe/Desktop/Programação/programming/IA/curso_vai_na_web/algoritmo_genetico/salarios.csv")
    df = df.drop(columns=["AMOSTRA"]) # Retira a coluna amostra

    return df.values.tolist()  # retorna somente o data frame

def fitness(individuo):
    erro_quadrado = 0
    a, b, c = individuo

    for experiencia, estudo, salario_real in conjunto_treino:
        salario_previsto = a*experiencia + b*estudo + c
        erro_quadrado += (salario_real - salario_previsto)**2

    mse = erro_quadrado/len(conjunto_treino)

    return (1/mse, individuo) # retorna uma tupla, que parece um array, mas é imutavel

def calcular_fitness_populacao(populacao):

    return [ fitness(individuo) for individuo in populacao]

def cruzamento(individuo1, individuo2):
    a1, b1, c1 = individuo1
    a2,b2,c2 = individuo2

    a = (a1 + a2) / 2
    b = (b1 + b2) / 2
    c = (c1 + c2) / 2

    return [a, b, c]


def mutacao(individuo):
    taxa_mutacao = 0.1

    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:  # gera um evento randomico na taxa desejada
            individuo[i] = random.gauss(0,100) # função gauss mede a distribuição gaussiana na média de dispersões]

    return individuo

def selecionar_melhores(fitness_populacao):
    return sorted(fitness_populacao)[-2:]

def criar_nova_geracao(melhores, tamanho=100):
    nova_geracao = [individuo for _, individuo in melhores]
    while len(nova_geracao) < tamanho:

        p1 = random.choice(melhores)[1]
        p2 = random.choice(melhores)[1]

        filho = cruzamento(p1, p2)
        filho = mutacao(filho)
        nova_geracao.append(filho)

    return nova_geracao

conjunto_treino = ler_csv()
populacao = criar_populacao()

historico_mse = []
melhor_global = None

# Geração é uma passada completo por todos os pontos de treino
#em outro algoritmos, sempre que passarmos um treino por toda uma população, será chamado época

for geracao in range(10):
    fitness_populacao = calcular_fitness_populacao(populacao)
    melhores = selecionar_melhores(fitness_populacao)

    if melhor_global is None or melhores[0][0] > melhor_global[0]:
        melhor_global = melhores[-1]

    mse = 1/melhor_global[0]

    historico_mse.append(mse)
    populacao = criar_nova_geracao(melhores)

    print("Melhor solução encontrada")
    print(f"a = {melhor_global[1][0]: .2f}")
    print(f"b = {melhor_global[1][1]: .2f}")
    print(f"c = {melhor_global[1][2]: .2f}")


plt.figure(figsize=(10,5))
plt.plot(historico_mse)
plt.title('MSE')
plt.xlabel("Geração")
plt.ylabel("MSE")
plt.grid(True)
plt.show()

# Gráfico não cai mais advém da dispersão talvez
# ou  talvez pelo modelo linear não ser o adequado
# O resultado é um plano tendo em vista a quantidade de variaveis

#brincar com os valores de mutação, valores de população, uma grande ou pequena
#mexer no tamanho

# Esse não é um algoritmo determinístico
# Está dentro de valores aproximados que ficam dentro de um erro aceitável, indicado pelo mse
# se o erro não cair, talvez seja necessário um melhor modelo ou um com menor dispersão

# Não é um algoritmo de convergencia rapida
# Quase sempre converge, mesmo que lentamente

# Em algoritmos que voce não conhece os criterios de convergencia, algortimo genetico
# pode ajudar. Porém, não é muito utilizado devido à performance

# Tem modelos de regressão linear, polinomial, exponencial, etc

