#!/usr/bin/env python

'''
Feature-based image matching sample.
Note, that you will need the https://github.com/opencv/opencv_contrib repo for SIFT and SURF
USAGE
  find_obj.py [--feature=<sift|surf|orb|akaze|brisk>[-flann]] [ <image1> <image2> ]
  --feature  - Feature to use. Can be sift, surf, orb or brisk. Append '-flann'
               to feature name to use Flann-based matcher instead bruteforce.
  Press left mouse button on a feature point to see its matching point.
'''

# Python 2/3 compatibility
from __future__ import print_function

import sys
import numpy as np
import cv2 as cv


class FindObj():
    '''Classe que encontra informacoes sobre a localizacao de um objeto'''
    def init_feature(self, name):
        '''Inicializa a classe quanto aos argumentos'''

        flann_index_kdtree = 1  # bug: flann enums are missing
        flann_index_lsh = 6

        chunks = name.split('-')

        if chunks[0] == 'sift':
            detector = cv.xfeatures2d.SIFT_create()
            norm = cv.NORM_L2
        elif chunks[0] == 'surf':
            detector = cv.xfeatures2d.SURF_create(800)
            norm = cv.NORM_L2
        elif chunks[0] == 'orb':
            detector = cv.ORB_create(400)
            norm = cv.NORM_HAMMING
        elif chunks[0] == 'akaze':
            detector = cv.AKAZE_create()
            norm = cv.NORM_HAMMING
        elif chunks[0] == 'brisk':
            detector = cv.BRISK_create()
            norm = cv.NORM_HAMMING
        else:
            return None, None
        if 'flann' in chunks:
            if norm == cv.NORM_L2:
                flann_params = dict(algorithm=flann_index_kdtree, trees=5)
            else:
                flann_params = dict(
                    algorithm=flann_index_lsh,
                    table_number=6, # 12
                    key_size=12,     # 20
                    multi_probe_level=1
                ) #2
            matcher = cv.FlannBasedMatcher(flann_params, {})
            # bug : need to pass empty dict (#1329)
        else:
            matcher = cv.BFMatcher(norm)
        return detector, matcher

    def filter_matches(self, kp1, kp2, matches, ratio=0.75):
        '''Aplica filtros para localizacao'''
        mkp1, mkp2 = [], []
        for item in matches:
            if len(item) == 2 and item[0].distance < item[1].distance * ratio:
                item = item[0]
                mkp1.append(kp1[item.queryIdx])
                mkp2.append(kp2[item.trainIdx])
        point1 = np.float32([kp.pt for kp in mkp1])
        point2 = np.float32([kp.pt for kp in mkp2])
        return point1, point2

    def extracao(self, img1, high=None):
        '''Extrai as coordenadas do objeto'''
        height, width = img1.shape[:2]
        limpo = np.int32([[0, 0], [0, 0]])
        if high is not None:
            corners = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
            corners = np.int32(
                cv.perspectiveTransform(corners.reshape(1, -1, 2), high).reshape(-1, 2) + (width, 0)
            )
            limpo = corners
            limpo[0][0] = limpo[0][0] - width
            limpo[1][0] = limpo[1][0] - width
            limpo[2][0] = limpo[2][0] - width
            limpo[3][0] = limpo[3][0] - width

        return limpo


def main(name, img1, img2):
    '''Prepara variaveis e valores'''
    null = np.int32([[0, 0], [0, 0]])
    detector, matcher = FindObj.init_feature(name)

    # if img1 is None:
    #     print('Find_obj=Failed to load fn1:', img1)
    #     sys.exit(1)

    # if img2 is None:
    #     print('Find_obj=Failed to load fn2:', img2)
    #     sys.exit(1)

    if detector is None:
        print('Find_obj=unknown feature:', name)
        sys.exit(1)

    kp1, desc1 = detector.detectAndCompute(img1, None)
    kp2, desc2 = detector.detectAndCompute(img2, None)
    null[0][0] = -999

    def match_and_draw():
        '''Encontra os pontos para extracao da imagem'''
        raw_matches = matcher.knnMatch(desc1, trainDescriptors=desc2, k=2)
        p1, p2 = FindObj.filter_matches(kp1, kp2, raw_matches)
        if len(p1) >= 6:
            H, status = cv.findHomography(p1, p2, cv.RANSAC, 5.0)
            print('%d / %d  inliers/matched' % (np.sum(status), len(status)))
        else:
            H, status = None, None
            print('%d matches found, not enough for homography estimation' % len(p1))
            return null
        return FindObj.extracao(img1, H)

    return match_and_draw()
