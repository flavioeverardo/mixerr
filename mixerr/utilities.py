from . import graph
from . import distance
from math import log10

def build_instance(answer_sets, k, size, diagonals, plain_approach):
    print("Calculating distances...")
    instance = ""
    min_distance = 0
    max_distance = 0
    if plain_approach:
        distancesText, min_distance, max_distance = distance.calculate_distances(answer_sets, k)
        instance += distancesText

    print("Searching for the optimum grid...")

    my_graph = graph.Graph((size,size), diagonals)
    my_graph = my_graph.nodes

    ## Set the constant
    instance += "%% Set the size of the map\n"
    #instance += "#const _n=%s.\n"%size
    instance += "size(%s).\n"%size
    instance += ""

    map = {}

    ## Get nodes
    instance += "%% Answer sets to fill the map.\n"
    for i in range(len(answer_sets)):
        instance += "answer_set(%s).\n"%(i+1)

    instance += "\n"
    instance += "%% Nodes in the map\n"
    node_id = 1
    for key, value in my_graph.items():
        instance += "node(%s).\n"%(node_id)
        map[key] = node_id
        node_id+=1

    instance += "\n"
    instance += "%% Bidirectional edges from the map.\n"

    ## Get edges
    edges = []
    for key, value in map.items():
        for node in my_graph[key]:
            if(value < map[node]):
                if plain_approach:
                    instance += "edge(%s,%s).\n"%(value, map[node])
                ## Get the edges to calculate the distance factor
                edges.append([value-1,map[node]-1])

    return instance, edges, min_distance, max_distance

def get_numbers_sequence(n, inf, sup):
    output = []
    if n > 1:
        continuous_difference = (sup-inf)/n
        initial = inf
        final = sup

        output.append(initial)
        for _ in range(n):
            output.append(initial + continuous_difference)
            initial += continuous_difference
    
        return output
    else:
        return None


def truthtable (n):
  if n < 1:
    return [[]]
  subtable = truthtable(n-1)
  return [ row + [v] for row in subtable for v in [0,1] ]


def dBFS2Gain(dBFS):
    return pow(10, dBFS/20)
    
def gain2dBFS(gain):
    dbfs = "%.2f"%(log10(gain) * 20)
    return dbfs
