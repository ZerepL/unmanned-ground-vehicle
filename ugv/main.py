import find_obj
import sys
import cv2 as cv
import camera
import motores

find = find_obj
cam = camera

img1 = './BaseD.jpg'
esquerda = './esquerda.jpg'
direita = './direita.jpg'
chegou = './chegou.jpg'

picExt = cam.tirafoto()

img1 = cv.imread(img1, 0)
esquerda = cv.imread(esquerda, 0)
direita = cv.imread(direita, 0)
chegou = cv.imread(chegou, 0)
img2 = cv.cvtColor(picExt, cv.COLOR_BGR2GRAY)

busca = find.main('sift', img1, img2)
height, width = img2.shape[:2]
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
        print('Direcao nao encontrada')
        sys.exit(1)

print(direcao)



# print('---------------------------------------------------------')
# print("Procurando direcao")
# direcao = arrowRecog.direcao_seta(crop_img)
# print('Direcao da seta: ')
# print(direcao)
# print('---------------------------------------------------------')
# motores.virar(direcao)

