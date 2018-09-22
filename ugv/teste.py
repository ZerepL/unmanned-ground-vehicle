import find_obj
import sys, getopt
import cv2 as cv
import arrowRecog

find = find_obj

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

limpo, limpoinfo = find.main('sift', img1, img2)
#crop_img = img2[(limpo[0][1]+16):(limpo[2][1]-15), (limpo[0][0]+8):(limpo[2][0]-8)]
crop_img = img2[(limpo[0][1]+16):(limpo[2][1]-15), (limpo[0][0]+8):(limpo[2][0]-70)]



print('---------------------------------------------------------')
print('Contem a imagem em:')
print(limpo)
print('---------------------------------------------------------')
print('Contem a informacao em: ')
print(limpoinfo)
print('---------------------------------------------------------')
print('Direcao da seta: ')
print(arrowRecog.direcao_seta(crop_img))
