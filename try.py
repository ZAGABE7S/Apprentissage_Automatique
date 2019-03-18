import math
import csv
import numpy as np
import pandas as pd
import sys
import os

def checkConformite():
    if len(sys.argv)<4:
        print("le nombre de parametre est insuffisant!")
        sys.exit(1)
    if not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
        print("le parametre 1 ou 2 n'est pas un fichier")
        sys.exit(1)
    try:
        k=int(sys.argv[3])
    except:
        print("Donnez une valeur entiere pour le k voisin")
        sys.exit(1)

def notIn(indic,liste):
    for j in range(len(liste)):
        if indic ==liste[j]:
            return True
    return False  

def getAllClass(liste):
    tmp=[]
    for i in range(len(liste)):
        if liste[i] not in tmp:
            tmp.append(liste[i])
    return tmp

def giveTheOccurrence(liste):
    occ=[]
    tmp=[]
    indice=[]
    for i in range(len(liste)):
        if liste[i] in tmp:
            tmp1=[y for y,j in enumerate(tmp) if j==liste[i]]
            occ[tmp1[0]]=int(occ[tmp1[0]])+1
        else:
            tmp.append(liste[i])
            occ.append(1) 
            indice.append(i)

    maxi=max(occ)
    ind=[i for i,j in enumerate(occ) if j==maxi]
    el=tmp[indice[ind[0]]]

    return el

def giveClassForGivenIndice(classe,indice):
    tmp=[]
    for i in indice:
        tmp.append(classe[i])
    return tmp   

def minima(tabe):
    #print(tabe)
    tmp=-1
    indice=[]
    max=1000000000000000000000000
    while len(indice)<k_v:
        max=1000000000000000000000000
        for i in range(len(tabe)):
            if(max>=tabe[i] and notIn(i,indice)==False ):
                tmp=i
                max=tabe[i]
        #del tabe[tmp] 
        indice.append(tmp)       
    return indice  
def knn2(points,tab_points):
    #print("point:",point1)
    #print("points:",tab_point)
    
    dist=[]
    
    for i in range(len(points)):
        tab_dist=[]
        for j in range(len(tab_points)):
            tmp=0
            for k in range(points.shape[1]-1):
                tmp=tmp+abs(float(points.iloc[i,k])-float(tab_points.iloc[j,k]))
                #print("abs(",points.iloc[i,k]," -",tab_points.iloc[j,k],")=",tmp)
            tab_dist.append(tmp)  
        dist.append(tab_dist)      
    return dist  

checkConformite()

train=pd.read_csv(sys.argv[1])
test=pd.read_csv(sys.argv[2])
k_v=int(sys.argv[3])
distance=knn2(test,train)

#------------------------------------------------
nn=np.array(train.iloc[:,-1])
nn=getAllClass(nn)
nn.sort()
print("les classes:",nn)
matrix=np.zeros((len(nn),len(nn)),dtype=int)

precision=0
for v in range(len(distance)):
    ind=minima(distance[v])
    #print("indice minima est:",ind)
    #print(distance[0])
    c=len(train.columns)-1
    #on recupere les classe des distance calculer---

    print("les indice des k voisin:",ind)
    classe_train=np.array(train.iloc[:,-1])
    class_test=np.array(test.iloc[:,-1])
    classe_d=giveClassForGivenIndice(classe_train,ind)
    predic=giveTheOccurrence(classe_d)
    true_val=class_test[v]
    if(predic==true_val):precision=precision+1

    print(classe_d," ------- ",predic," : ",true_val)

print("la precision est de:",precision," ",len(distance)," ",float(precision)/float(len(distance)))
p=float(precision)/float(len(distance))
print("voici le rappel:",float(precision)/float(len(train)))  
r= float(precision)/float(len(train))
f=(2*(r*p))/(p+r)
print("la mesure F:",f)