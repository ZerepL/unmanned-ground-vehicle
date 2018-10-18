#import camera
#import motores
import dijsktra
#import cv2 as cv
baseA = './baseA.jpg'
baseB = './baseB.jpg'
baseC = './baseC.jpg'
baseD = './baseD.jpg'

def converte(path):
    path_refinado = []
    for item in path:
        if item == "a":
            path_refinado.append(baseA)
        elif item == "b":
            path_refinado.append(baseB)
        elif item == "c":
            path_refinado.append(baseC)
        elif item == "d":
            path_refinado.append(baseD)

    return path_refinado

graph = dijsktra.Graph([])
graph.add_edge("a", "b", 4)
graph.add_edge("a", "c", 1)
graph.add_edge("b", "c", 5)
graph.add_edge("b", "d", 1)
graph.add_edge("c", "d", 1)

path =(graph.dijkstra("a", "b"))
path_refina = converte(path)
print(path_refina)

