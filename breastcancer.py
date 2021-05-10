import numpy as np
import pandas as pd
import ML
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import pygraphviz as pgv
breast_cancer = pd.read_csv('breast-cancer.txt')
breast_cancer = breast_cancer[['Age','Menopause','Tumor Size','Inv. Nodes','Node Caps','Deg. Malig.','Breast','Breast Quadrant','Irradiate','Class']]
ML.crear_arbol(breast_cancer, 'breast-cancerID3')