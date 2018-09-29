import find_obj
import sys, getopt
import cv2 as cv
import arrowRecog
#import camera
import motores

find = find_obj
#cam = camera

#picExt = cam.tirafoto()

opts, args = getopt.getopt(sys.argv[1:], '', ['feature='])
opts = dict(opts)
feature_name = opts.get('--feature', 'brisk')
try:
    fn1, fn2 = args
except:
    print('falha na importacao das imagens')
    sys.exit(1)

img1 = cv.imread(fn1, 0)
img2 = cv.imread(fn2, 0)

#img2 = cv.cvtColor(picExt, cv.COLOR_BGR2GRAY)
print('---------------------------------------------------------')
print("Procurando por padrao")
limpo, limpoinfo = find.main('sift', img1, img2)

if (limpo[0][0]==limpoinfo[0][0]).all():
    sys.exit(1)
else:
    print("Padrao encontrado")
    print(limpoinfo)
    crop_img = img2[(limpo[0][1]+16):(limpo[2][1]-15), (limpo[0][0]+8):(limpo[2][0]-70)]

print('---------------------------------------------------------')
print("Procurando direcao")
direcao = arrowRecog.direcao_seta(crop_img)
print('Direcao da seta: ')
print(direcao)
print('---------------------------------------------------------')
motores.virar(direcao)

