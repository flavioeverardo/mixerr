from prettytable import PrettyTable
from . import distance
from . import util
import numpy as np
import matplotlib.pyplot as plt

def build_table(clusters, size, display):

    ## improve this with numpy
    myTable = PrettyTable()
    myTable.header = False
    myTable.hrules = True

    id = 0
    row = []
    i = 0

    for cluster in clusters:
        res = ' '.join([str(elem) for elem in sorted(cluster)])
        row.append(res)
        id += 1
        
        if id == size:
            myTable.add_row(row)
            row = []
            id = 0
        i +=1
    if display:
        print(myTable)


def build(model, all_models, edges, display):
    atoms_list = model.symbols(shown=True)
    
    size = 0
    for atom in atoms_list:
        if "size" in str(atom):
            size=int(str(atom.arguments[0]))
    
    clusters = [[] for i in range(size * size)]
    cluster_models = [[] for i in range(size * size)]
    
    similarity_factor = 0
    distance_factor = 0
    weights = [0] * size
    
    ## Interpret the results
    for atom in atoms_list:
        if "cluster" in str(atom):
            cluster = int(str(atom.arguments[0]))-1
            answer = int(str(atom.arguments[1]))
            clusters[cluster].append(answer)

            l = []
            for symbol in all_models[answer-1]:
                l.append(str(symbol))
            cluster_models[cluster].append(l)

    if display:
        print("Table: Answer sets per cluster")
    build_table(clusters, size, display)
    result = []
    for cluster in cluster_models:
        result.append(list(set.intersection(*[set(x) for x in cluster])))
        similarity_factor += distance.distances(cluster)

    for edge in edges:
        lists_to_compare = []
        for node in edge:
            a = cluster_models[node]
            for l in a:
                lists_to_compare.append(l)
        distance_factor += distance.distances(lists_to_compare)

    if display:
        print("Average clusters distance: %.2f"%(distance_factor/len(edges)))
        print("Total distances between clusters: %s"%distance_factor)
        print("-----------------------------------------------------------------------------------------------------------------------------------------")
