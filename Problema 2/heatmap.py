import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

lista_prueba = [[1,2], [3,4]]
x = np.array(lista_prueba)
uniform_data = np.random.rand(10, 10)

hm = sns.heatmap(x)
plt.show()