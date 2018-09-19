import numpy as np
import cv2 as cv
import find_obj
import sys, getopt

find = find_obj.findObj()

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
detector, matcher = find.init_feature(feature_name)

if img1 is None:
    print('Failed to load fn1:', fn1)
    sys.exit(1)

if img2 is None:
    print('Failed to load fn2:', fn2)
    sys.exit(1)

if detector is None:
    print('unknown feature:', feature_name)
    sys.exit(1)

print('using', feature_name)

kp1, desc1 = detector.detectAndCompute(img1, None)
kp2, desc2 = detector.detectAndCompute(img2, None)
print('img1 - %d features, img2 - %d features' % (len(kp1), len(kp2)))

def match_and_draw():
    print('matching...')
    raw_matches = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2) #2
    p1, p2 = find.filter_matches(kp1, kp2, raw_matches)
    if len(p1) >= 4:
        H, status = cv.findHomography(p1, p2, cv.RANSAC, 5.0)
        print('%d / %d  inliers/matched' % (np.sum(status), len(status)))
    else:
        H, status = None, None
        print('%d matches found, not enough for homography estimation' % len(p1))

    limpo, limpoinfo = find.extracao(img1, H)

    print('---------------------------------------------------------')
    print('Contem a imagem em:')
    print(limpo)
    print('---------------------------------------------------------')
    print('Contem a informacao em:')
    print(limpoinfo)

match_and_draw()