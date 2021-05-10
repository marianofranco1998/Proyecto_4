import numpy as np
import pandas as pd
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import pygraphviz as pgv

#Dado un dataframe y el indice de una columna, 
#calcula la entropia de dicha columna
# arr :  Dataframe
# n   :  indice de la columna 
def entropia(arr,n):
    #types_col es una pd.Series que tiene todos los valores de un atributo
    # asi como la cantidad de veces que aparece
    types_col = arr.iloc[:,n].value_counts()
    tot = sum(types_col)

    #a es el nombre del atributo/columna n-esima
    #b es el nombre del atributo/columna a clasificar
    a = arr.columns[n]
    b = arr.columns[-1]
    #manip es una serie que tiene como clave 
    # el valor del atributo y el valor de la clasificacion
    # es decir, ayuda a clasificar cuantos hay de cada clasificacion
    # por cada valor del atributo
    manip = arr.groupby([a,b]).size()

    entrp = 0

    for label,content in types_col.iteritems():
        logs = 0
        for label_2,content_2 in manip.iteritems():
            if label == label_2[0]:
                c = (content_2/content)
                logs += c*np.log2(c)

        entrp += (content/tot)*(-logs)

    return entrp

background = '#DDE5E7'
end_node = '#D4674C'
int_node = '#67727E'
undetermined_node = '#000000' #'#c66900'
indx = 0
reglasDeInferencia = []
arbol_labels = []
arbol_aristas = []
def crear_arbol(df, nombreImg):
    G = nx.DiGraph(bgcolor=background)
    global indx
    global reglasDeInferencia
    global arbol_labels
    global arbol_aristas
    arbol_aristas = []
    arbol_labels = []
    indx = 0
    reglasDeInferencia = []
    rec_crear_arbol(df,G, -1, 'f','Si ')

    G.graph['graph']={'rankdir':'TD'}
    G.graph['node']={'shape':'circle'}
    G.graph['edges']={'arrowsize':'4.0'}

    A = to_agraph(G)
    A.layout('dot')
    A.draw(nombreImg+'.png')
    #guardo las reglas de inferencia en un archivo
    fileReglas = open('reglas'+nombreImg+'.txt',"w")
    for i in reglasDeInferencia:
        fileReglas.write(i+'\n')
    fileReglas.close()
    #guardo el arbol en un archivo
    fileArbolLabels = open(nombreImg+'arbolLabels.txt',"w")
    for i in arbol_labels:
        fileArbolLabels.write(str(i)+'\n')
    fileArbolLabels.close()
    
    fileArbolAristas = open(nombreImg+'arbolAristas.txt',"w")
    for i in arbol_aristas:
        fileArbolAristas.write(str(i)+'\n')
    fileArbolAristas.close()
    return arbol_labels, arbol_aristas


#función recursiva que crea el arbol de ID3
#Parametros:
#   df:     dataframe que representa la subtabla desde la que se crea el subarbol
#   G:      es el arbol que estamos creando
#   parent: indice del nodo padre 
#   lab:    etiqueta que tendra la arista con la que se conecta este subarbol con el nodo padre
#   indx:   indice del siguiente nodo a crear (cada nodo debe tener un unico id)
def rec_crear_arbol(df, G, parent, lab, regla):
    #casos bases para saber si estamos en una hoja:
    #   todos las entradas tienen la misma clasificación (pueden haber mas de una columna)
    #   solo hay una columna
    #si no es un caso base, elegimos la columna de menor entropia 
    #y mandamos a recrear el arbol con el resto de subtablas
    global indx
    global reglasDeInferencia

    global arbol_labels
    global arbol_aristas
    # Checamos que la columna de classificación tenga un solo valor, si este es el caso, link up y BREAK
    arr_check = df.iloc[:,-1].unique()
    if len(arr_check) == 1:
        reglasDeInferencia.append(regla + " => "+str(arr_check[0]))
        #en el indice indx de las listas arbol_ voy a guardar la informacion de este nodo
        arbol_labels.append(arr_check[0])
        arbol_aristas.append([]) 

        #agrego la arista al nodo de mi padre
        arbol_aristas[parent].append([lab, indx])

        #ahora agrego los nodos a la grafica
        G.add_node(indx,label=arr_check[0],style='filled',fillcolor=end_node,penwidth=0,fontcolor=background)
        G.add_edge(parent,indx,label=lab,fontcolor=int_node,arrowhead='open',color=int_node)
        indx+=1
        return
    #eliminamos todas las columnas(atributos) que solo tienen un valor
    # estas no ayudan a clasificar (la columna de clase no puede ser eliminada pues ya verificamos que no tuviera un unico valor)
    df=df[[i for i in df if len(set(df[i]))>1]]

    #si ya no hubiera filas, acabamos la dfs
    if df.shape[0] == 0:
        return

    # Si solo hay una columna entonces es la columna de resultados
    # este es un caso raro, pues quiere decir que una combinacion de atributos da resultados distintos
    # lo que hacemos es desplegar la probabilidad de cada resultado
    if df.shape[1] == 1:
        #decimos que el metodo no es concluyente
        #agregamos la etiqueta y creamos el nodo para las aristas de este nodo
        arbol_aristas.append([])
        arbol_labels.append('No concluyente')
        #agregamos la arista al padre
        arbol_aristas[parent].append([lab, indx])
        

        G.add_node(indx,label='No concluyente',style='filled',fillcolor=undetermined_node,penwidth=0,fontcolor=background)
        G.add_edge(parent,indx,label=lab,fontcolor=int_node,arrowhead='open',color=int_node)
        indxNoC = indx
        indx += 1
        
        #vemos cuantos hay de cada clasifición
        value_counts = df[df.columns[-1]].value_counts()
        tot = sum(value_counts)
        
        #creamos un nodo para cada clasificación con su respectiva probabilidad 
        for value, count in value_counts.iteritems():
            #para este nodo ya no guardamos indices a los siguientes nodos
            #directamente guardamos el valor asociado a cada probabilidad en lugar del indice
            #agrego a las listas para que indice esté  sincronizada con la posicion en la lista
            arbol_aristas[indxNoC].append([str(round(count/tot*100,2)), indx]) 
            arbol_aristas.append([])
            arbol_labels.append(value)
            G.add_node(indx,label=value,style='filled',fillcolor=end_node,penwidth=0,fontcolor=background)
            G.add_edge(indxNoC, indx,label=str(round(count/tot*100,2)),fontcolor=int_node,arrowhead='open',color=int_node)
            indx += 1
        return

    #si cadan atributos todavia, tomamos el de entropía mínima
    # Calculamos la entropía mínima de las columnas restantes NO de classificación
    cols = len(df.columns) - 1
    min_ent = entropia(df,0)
    col_min_ent = 0
    for i in range(1,cols):
        new_ent = entropia(df,i)
        if min_ent > new_ent:
            min_ent = new_ent
            col_min_ent = i

    #obtenemos la etiqueta/nombre de este atributo
    child = df.columns[col_min_ent]
    arbol_labels.append(child)
    arbol_aristas.append([])
    #agregamos la arista al padre
    if parent != -1:
        arbol_aristas[parent].append([lab, indx])
    
    #lo agregamos a la grafica
    G.add_node(indx,label=child,style='filled',fillcolor= int_node,penwidth=0,fontcolor=background)
    if parent != -1:
        G.add_edge(parent,indx,label=lab,fontcolor=int_node,arrowhead='open',color=int_node)
    
    #obtenemos todos los valores del atributo de menor entropia
    values = df.iloc[:,col_min_ent].unique()
    #guardamos el indice para mandarlo como parametro en la recursion 
    indxMinE = indx
    indx += 1
    for k in values:
        rec_df = df[ df[child] == k ].drop(child,axis=1)
        rec_crear_arbol(rec_df,G, indxMinE, k, regla +'('+str(child)+' = '+str(k)+') AND ')
    
    """
    if min_ent == 0:
        classes = []
        # con df[child] == k seleccionamos los registros que tenga un valor k en el atributo
        # de menos entropia, y como tienen entropia 0, elegimos el valor de la categoria
        # del primero de ellos (que de hecho es la categoria del de todos por ser de entropia 0)
        for k in values:
            classes.append( df[ df[child] == k ].iloc[0,-1])
        
        #realmente esto podriamos dejarlo a la siguiente llamada recursiva, pero lo hacemos aqui para
        #disminuir los recursos de ejecución
        #aqui agregamos las hojas de este subarbol 
        
        for k,l in zip(values,classes):
            reglasDeInferencia.append(regla +'('+str(child)+'='+str(k)+') => '+l)
            G.add_node(indx,label=l,style='filled',fillcolor=end_node,penwidth=0,fontcolor=background)
            G.add_edge(indxMinE, indx,label=k,fontcolor=int_node,arrowhead='open',color=int_node)
            indx += 1
    else:
        for k in values:
            rec_df = df[ df[child] == k ].drop(child,axis=1)
            rec_crear_arbol(rec_df,G, indxMinE, k, regla +'('+str(child)+' = '+str(k)+') AND ')
    """
    return 