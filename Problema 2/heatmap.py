import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat

def heatmap_de_super(super, **kwargs):
    distribucion_demandas = super.generar_heatmap()
    df = pd.DataFrame(np.array(distribucion_demandas), 
                    columns = ['P' + str(x) for x in range(1,16)],
                    index=[str(x) for x in range(1,18)])

    if 'axis' in kwargs:
        axis = kwargs.get('axis')
        heat_map = sns.heatmap(df, robust=True, linewidths=0.05, annot_kws={'fontsize':12}, fmt='', cmap="rocket_r", ax=axis)
    else:
        heat_map = sns.heatmap(df, robust=True, linewidths=0.05, annot_kws={'fontsize':12}, fmt='', cmap="rocket_r")

    return heat_map

def heatmap_de_super_pasillos(super, **kwargs):
    distribucion_demandas_por_pasillo = super.heatmap_pasillos()
    df_pasillos = pd.DataFrame(np.array(distribucion_demandas_por_pasillo), 
                    columns = ['P' + str(x) for x in range(1,16)],
                    index=['A', 'B'])

    if 'axis' in kwargs:
        axis = kwargs.get('axis')
        heat_map = sns.heatmap(df_pasillos, robust=True, linewidths=0.05, cmap="rocket_r", ax=axis)
    else:
        heat_map = sns.heatmap(df_pasillos, robust=True, linewidths=0.05, cmap="rocket_r")
    
    return heat_map

def generar_figura_completa(super, titulo):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,7))
    fig.suptitle(titulo, fontsize=18)
    ax1.set_title("Heatmap Secciones")
    ax2.set_title("Heatmap Pasillos")

    text_var_demanda_por_seccion = ("Desv. Est. demanda por sección: " + str(super.stdev_por_seccion()))
    text_var_demanda_por_pasillo = ("Desv. Est. demanda por pasillo: " + str(super.stdev_por_pasillo()))
    text_promedio_stdev_por_seccion = "Promedio de desviacion estandar por seccion: " + str(super.promedio_stdev_por_seccion())
    text_promedio_stdev_por_pasillo = "Promedio de desviacion estandar por pasillo: " + str(super.promedio_stdev_por_pasillo())
    text_distancia_prom = "Distancia recorrida promedio: " + str(super.dict_distacia["promedio"])
    text_distancia_max_min = (f"Distancia recorrida [min, max]: [{super.dict_distacia['min']},{super.dict_distacia['max']}]")

    heat_map_1 = heatmap_de_super(super, axis=ax1)
    heat_map_2 = heatmap_de_super_pasillos(super, axis=ax2)

    ax1.set_xlabel(text_var_demanda_por_seccion + '\n' + text_promedio_stdev_por_seccion + '\n' + text_distancia_prom,
     position=(0., 1e6), horizontalalignment='left')
    ax2.set_xlabel(text_var_demanda_por_pasillo + '\n' + text_promedio_stdev_por_pasillo + '\n' + text_distancia_max_min,
     position=(0., 1e6), horizontalalignment='left')

    return fig

#Heatmaps considerando 11.400 permanentes

def heatmap_de_super_estacional(super, **kwargs):
    distribucion_demandas = super.generar_heatmap_estacional()
    df = pd.DataFrame(np.array(distribucion_demandas), 
                    columns = ['P' + str(x) for x in range(1,16)],
                    index=[str(x) for x in range(1,18)])

    color = sns.color_palette("rocket_r", as_cmap=True)
    #color.set_over('blue')
    #sns.heatmap(np.random.uniform(0, 0.07, (1, 20)), square=True, linewidths=.5, annot=True, fmt='.3f',
            #cmap=green, vmin=0, vmax=0.05, cbar_kws={'extend': 'max'})

    if 'axis' in kwargs:
        axis = kwargs.get('axis')
        heat_map = sns.heatmap(df, robust=True, linewidths=0.05, annot_kws={'fontsize':12}, fmt='', cmap=color, ax=axis, vmax=10000)
    else:
        heat_map = sns.heatmap(df, robust=True, linewidths=0.05, annot_kws={'fontsize':12}, fmt='', cmap=color)

    return heat_map

def heatmap_de_super_pasillos_estacional(super, **kwargs):
    distribucion_demandas_por_pasillo = super.heatmap_pasillos()
    df_pasillos = pd.DataFrame(np.array(distribucion_demandas_por_pasillo), 
                    columns = ['P' + str(x) for x in range(1,16)],
                    index=['A', 'B'])

    if 'axis' in kwargs:
        axis = kwargs.get('axis')
        if 'center' in kwargs:
            center = kwargs.get('center')
            heat_map = sns.heatmap(df_pasillos, robust=True, linewidths=0.05, cmap="rocket_r", ax=axis, center=center)
        else:
            heat_map = sns.heatmap(df_pasillos, robust=True, linewidths=0.05, cmap="rocket_r", ax=axis)
    else:
        heat_map = sns.heatmap(df_pasillos, robust=True, linewidths=0.05, cmap="rocket_r")
    
    return heat_map

def generar_figura_completa_estacional(super, titulo):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,7))
    fig.suptitle(titulo, fontsize=18)
    ax1.set_title("Heatmap Secciones")
    ax2.set_title("Heatmap Pasillos")

    
    text_var_demanda_por_seccion = ("Desv. Est. demanda por sección: " + str(super.stdev_por_seccion_estacional()))
    text_var_demanda_por_pasillo = ("Desv. Est. demanda por pasillo: " + str(super.stdev_por_pasillo_estacional()))
    text_promedio_stdev_por_seccion = "Promedio de desviacion estandar por seccion: " + str(super.promedio_stdev_por_seccion_estacional())
    text_promedio_stdev_por_pasillo = "Promedio de desviacion estandar por pasillo: " + str(super.promedio_stdev_por_pasillo_estacional())
    #text_distancia_prom = "Distancia recorrida promedio: " + str(super.dict_distacia["promedio"])
    #text_distancia_max_min = (f"Distancia recorrida [min, max]: [{super.dict_distacia['min']},{super.dict_distacia['max']}]")
    
    heat_map_1 = heatmap_de_super_estacional(super, axis=ax1)
    heat_map_2 = heatmap_de_super_pasillos_estacional(super, axis=ax2)

    #ax1.set_xlabel(text_var_demanda_por_seccion + '\n' + text_promedio_stdev_por_seccion + '\n' + text_distancia_prom,
    # position=(0., 1e6), horizontalalignment='left')
    #ax2.set_xlabel(text_var_demanda_por_pasillo + '\n' + text_promedio_stdev_por_pasillo + '\n' + text_distancia_max_min,
    # position=(0., 1e6), horizontalalignment='left')

    ax1.set_xlabel(text_var_demanda_por_seccion + '\n' + text_promedio_stdev_por_seccion,
     position=(0., 1e6), horizontalalignment='left')
    ax2.set_xlabel(text_var_demanda_por_pasillo + '\n' + text_promedio_stdev_por_pasillo,
     position=(0., 1e6), horizontalalignment='left')

    return fig

def generar_figura_completa_estacional_stdev(super, titulo):
    fig, (ax1) = plt.subplots(1, 1, figsize=(14,7))
    fig.suptitle(titulo, fontsize=18)
    ax1.set_title("Heatmap Desviaciones Estandar")

    
    text_var_demanda_por_seccion = ("Desv. Est. demanda por sección: " + str(super.stdev_por_seccion_estacional()))
    text_var_demanda_por_pasillo = ("Desv. Est. demanda por pasillo: " + str(super.stdev_por_pasillo_estacional()))
    text_promedio_stdev_por_seccion = "Promedio de desviacion estandar por seccion: " + str(super.promedio_stdev_por_seccion_estacional())
    text_promedio_stdev_por_pasillo = "Promedio de desviacion estandar por pasillo: " + str(super.promedio_stdev_por_pasillo_estacional())
    #text_distancia_prom = "Distancia recorrida promedio: " + str(super.dict_distacia["promedio"])
    #text_distancia_max_min = (f"Distancia recorrida [min, max]: [{super.dict_distacia['min']},{super.dict_distacia['max']}]")
    
    distribucion_stdev = super.generar_heatmap_estacional_stdev()
    df = pd.DataFrame(np.array(distribucion_stdev), 
                    columns = ['P' + str(x) for x in range(1,16)],
                    index=[str(x) for x in range(1,18)])

    color = sns.color_palette("rocket_r", as_cmap=True)
    heat_map = sns.heatmap(df, robust=True, linewidths=0.05, annot_kws={'fontsize':12}, fmt='', cmap=color, ax=ax1, square=True, center=220)

    #ax1.set_xlabel(text_var_demanda_por_seccion + '\n' + text_promedio_stdev_por_seccion + '\n' + text_distancia_prom,
    # position=(0., 1e6), horizontalalignment='left')
    #ax2.set_xlabel(text_var_demanda_por_pasillo + '\n' + text_promedio_stdev_por_pasillo + '\n' + text_distancia_max_min,
    # position=(0., 1e6), horizontalalignment='left')

    ax1.set_xlabel(text_var_demanda_por_seccion + '\n' + text_promedio_stdev_por_seccion + '\n' + text_var_demanda_por_pasillo + '\n' + text_promedio_stdev_por_pasillo,
     position=(0., 1e6), horizontalalignment='left')

    return fig

def grafico_evolucion_varianza(varianzas):
    
    iteraciones = []
    for i in range(len(varianzas)):
        iteraciones.append(str(i))
    
    fig, (ax1) = plt.subplots(1, 1, figsize=(14,7))
    fig.suptitle('Evolución varianza por iteración', fontsize=18)
    
    ax1.ticklabel_format(useOffset=False, style='plain')
    ax1.plot(iteraciones, varianzas, color='blue', marker='o')
    plt.xlabel('Iteración', fontsize=14)
    plt.ylabel('Varianza demanda por sección', fontsize=14)
    plt.grid(True)
    plt.show()

def generar_figura_completa_estacional_optima(super, titulo, demanda_por_seccion):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,7))
    fig.suptitle(titulo, fontsize=18)
    ax1.set_title("Heatmap Secciones")
    ax2.set_title("Heatmap Pasillos")

    
    text_var_demanda_por_seccion = ("Desv. Est. demanda por sección: " + str(super.stdev_por_seccion_estacional()))
    #text_var_demanda_por_pasillo = ("Desv. Est. demanda por pasillo: " + str(super.stdev_por_pasillo_estacional()))
    #text_promedio_stdev_por_seccion = "Promedio de desviacion estandar por seccion: " + str(super.promedio_stdev_por_seccion_estacional())
    text_promedio_stdev_por_pasillo = "Promedio de desviacion estandar por pasillo: " + str(super.promedio_stdev_por_pasillo_estacional())
    #text_distancia_prom = "Distancia recorrida promedio: " + str(super.dict_distacia["promedio"])
    #text_distancia_max_min = (f"Distancia recorrida [min, max]: [{super.dict_distacia['min']},{super.dict_distacia['max']}]")
    
    heat_map_1 = heatmap_de_super_estacional(super, axis=ax1)
    heat_map_2 = heatmap_de_super_pasillos_estacional(super, axis=ax2, center=40000)

    #ax1.set_xlabel(text_var_demanda_por_seccion + '\n' + text_promedio_stdev_por_seccion + '\n' + text_distancia_prom,
    # position=(0., 1e6), horizontalalignment='left')
    #ax2.set_xlabel(text_var_demanda_por_pasillo + '\n' + text_promedio_stdev_por_pasillo + '\n' + text_distancia_max_min,
    # position=(0., 1e6), horizontalalignment='left')

    ax1.set_xlabel(text_var_demanda_por_seccion + '\n' + 'Demanda por sección: ' + str(demanda_por_seccion),
     position=(0., 1e6), horizontalalignment='left')
    ax2.set_xlabel(text_promedio_stdev_por_pasillo+ '\n' + 'Demanda por pasillo: ' + str(demanda_por_seccion*8) + ' o '+ str(demanda_por_seccion*9),
     position=(0., 1e6), horizontalalignment='left')

    return fig
