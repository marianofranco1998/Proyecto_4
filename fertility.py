## imports
import numpy as np
import pandas as pd
import ML
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import pygraphviz as pgv

## datos
original = pd.read_csv('fertility_Diagnosis.txt')
original.head()

def age(i):
    i = i*18+18
    if(i<=21):
        return "[18,21]"
    elif(i<=24):
        return "(21,24]"
    elif(i<=27):
        return "(24,27]"
    elif(i<=30):
        return "(27,30]"
    elif(i<=33):
        return "(30,33]"
    else:
        return "(33,36]"

original['AGE']=original['AGE'].apply(age)

def sitting(i):
    i = i*16
    if(i<=2):
        return "[0,2]"
    elif(i<=4):
        return "(2,4]"
    elif(i<=8):
        return "(4,8]"
    elif(i<=10):
        return "(8,10]"
    elif(i<=12):
        return "(10,12]"
    elif(i<=14):
        return "(12,14]"
    else:
        return "(14,16]"

original['SITTING']=original['SITTING'].apply(sitting)

def alcohol(i):
    switcher = {
        0.2: "several times a day",
        0.4: "every day",
        0.6: "several times a week",
        0.8: "once a week",
        1: "hardly ever or never"
    }
    return switcher.get(i)

original['ALCOHOL']=original['ALCOHOL'].apply(alcohol)

def season(i):
    switcher = {
        -1: "winter",
        -0.33: "spring",
        0.33: "summer",
        1: "fall"
    }
    return switcher.get(i)

original['SEASON']=original['SEASON'].apply(season)

original.head()
ML.crear_arbol(original, 'fertilityID3')