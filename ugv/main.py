import find_obj
import sys
import cv2 as cv
import camera
import motores
import dijsktra

find = find_obj
cam = camera

baseA = './baseA.jpg'
baseB = './baseB.jpg'
baseC = './baseC.jpg'
baseD = './baseD.jpg'
esquerda = './esquerda.jpg'
direita = './direita.jpg'
chegou = './chegou.jpg'
frente = './frente.jpg'

graph = dijsktra.Graph([])
graph.add_edge("a", "d", 4)
# graph.add_edge("a", "c", 1)
# graph.add_edge("b", "c", 5)
# graph.add_edge("b", "d", 1)
# graph.add_edge("c", "d", 1)

baseA = cv.imread(baseA, 0)
baseB = cv.imread(baseB, 0)
baseC = cv.imread(baseC, 0)
baseD = cv.imread(baseD, 0)
esquerda = cv.imread(esquerda, 0)
direita = cv.imread(direita, 0)
chegou = cv.imread(chegou, 0)
frente = cv.imread(frente, 0)

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

path = (graph.dijkstra("d", "a"))
path_limpo = converte(path)
ponto_atual = path_limpo[0]

while(ponto_atual != path_limpo[(len(path_limpo)-1)]):
    print('Lendo linhas')
    motores.lerlinhas()
    print('Tirando foto')
    y = 0
    picExt = cam.tirafoto()
    img2 = cv.cvtColor(picExt, cv.COLOR_BGR2GRAY)
    print(path[0])
    busca = find.main('sift', ponto_atual, img2) # <-------------------
    if busca[0][0] == -999:
        print("Nada encontrado")

        sys.exit(1) 
    else:
        print("Padrao encontrado")
        print(busca)
        crop_img = img2[busca[0][1]:busca[2][1], busca[0][0]:busca[2][0]]

    busca[0][0] = -999
    direcao = ''
    x = 0
    while(busca[0][0] == -999):

        if(x == 0):
            busca = find.main('sift', chegou, crop_img)
            x = 1
            direcao = 'chegou'
        elif (x == 1):
            busca = find.main('sift', direita, crop_img)
            x = 2
            direcao = 'direita'
        elif (x == 2):
            busca = find.main('sift', esquerda, crop_img)
            x = 3
            direcao = 'esquerda'
        elif (x == 3):
            busca = find.main('sift', frente, crop_img)
            x = 4
            direcao = 'frente'
        elif (x == 4):
            print('Direcao nao encontrada')
            direcao = 'nada'
    motores.virar(direcao)
    if direcao == 'chegou':
        print("Estacao %s alcancada" % (path[y]))
        y = y + 1
        ponto_atual = path_limpo[y]
