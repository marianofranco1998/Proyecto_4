import numpy as np
import pandas as pd
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import pygraphviz as pgv

def entropia(arr,n):
    types_col = arr.iloc[:,n].value_counts()
    tot = sum(types_col)

    a = arr.columns[n]
    b = arr.columns[-1]
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

def crear_arbol(df):
    G = nx.DiGraph(bgcolor=background)

    rec_crear_arbol(df,G, 'f', 'f')

    G.graph['graph']={'rankdir':'TD'}
    G.graph['node']={'shape':'circle'}
    G.graph['edges']={'arrowsize':'4.0'}

    A = to_agraph(G)
    A.layout('dot')
    A.draw('result_chido.png')

def rec_crear_arbol(df, G, parent, lab):
    
    id1 = np.random.rand()

    # Checamos que la columna de classificación tenga un solo valor, si este es el caso, link up y BREAK
    arr_check = df.iloc[:,-1].unique()
    if len(arr_check) == 1:
        G.add_node(id1,label=arr_check[0],style='filled',fillcolor=end_node,penwidth=0,fontcolor=background)
        G.add_edge(parent,id1,label=lab,fontcolor=int_node,arrowhead='open',color=int_node)
        return
    
    class_name = df.columns[-1]
    df=df[[i for i in df if len(set(df[i]))>1 or i == class_name]]

    # Si solo hay una columna entonces es la columna de resultados, BREAK
    if df.shape[1] == 1 or df.shape[0] == 0:
        return
    
    # Calculamos la entropía mínima de las columnas restantes NO de classificación
    cols = len(df.columns) - 1
    min_ent = entropia(df,0)
    col_min_ent = 0
    for i in range(1,cols):
        new_ent = entropia(df,i)
        if min_ent > new_ent:
            min_ent = new_ent
            col_min_ent = i


    values = df.iloc[:,col_min_ent].unique()

    child = df.columns[col_min_ent]
    G.add_node(id1,label=child,style='filled',fillcolor= int_node,penwidth=0,fontcolor=background)
    if parent != 'f':
        G.add_edge(parent,id1,label=lab,fontcolor=int_node,arrowhead='open',color=int_node)

    if min_ent == 0:
        classes = []
        for k in values:
            newdf = df.loc[df.iloc[:,col_min_ent] == k].iloc[:,-1]
            classes.append(newdf.unique()[0])
        
        for k,l in zip(values,classes):
            id2 = np.random.rand()
            G.add_node(id2,label=l,style='filled',fillcolor=end_node,penwidth=0,fontcolor=background)
            G.add_edge(id1,id2,label=k,fontcolor=int_node,arrowhead='open',color=int_node)
        return
    else:
    
        for k in values:
            rec_df = df.loc[df.iloc[:,col_min_ent] == k].drop(df.columns[col_min_ent],axis=1)
            rec_crear_arbol(rec_df,G,id1,k)