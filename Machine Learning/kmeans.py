import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv('/home/felipe/Desktop/Programação/programming/IA/curso_vai_na_web/Kmeans/Pokemon_stats.csv')

X = df[['Attack', 'Defense']]

kmeans = KMeans(n_clusters=5, random_state=10) # random_state é a minha "seed"
kmeans.fit(X)

df['Cluster'] = kmeans.labels_

plt.scatter(x = df['Attack'], y = df['Defense'], c=df['Cluster'],s = 100, alpha = 0.6) # Gráfico de dispersão
                                                              # 5 cores para poder separar os grupos
centroids = kmeans.cluster_centers_

plt.scatter(x = centroids[:, 0], y = centroids[:,1], color="black", marker="X", s=200)
plt.xlabel('Attack')
plt.ylabel('Defense')
plt.grid(True)

pokemon = [[50, 20]]
plt.show()

predict = kmeans.predict(pokemon)
print(f'O novo pokemon está no agrupamento: {predict.item()}')
