from data_work import ordenados
from model import *

import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

super = Supermercado()
super.poblar_fase_0(ordenados)

distribucion_demandas = super.generar_heatmap()
min_5, max_5 = top_5(distribucion_demandas)
guardar_distribucion(super, min_5, max_5, "fase_0.txt")
df = pd.DataFrame(np.array(distribucion_demandas), 
                    columns = ['P' + str(x) for x in range(1,16)],
                    index=[str(x) for x in range(1,18)])

#labels = df.applymap(lambda v: str(5 - (index_list.index(v)%10)) if v in index_list else '')

heat_map_1 = sns.heatmap(df, robust=True, linewidths=0.05, annot_kws={'fontsize':12}, fmt='', cmap="rocket_r")
plt.show()