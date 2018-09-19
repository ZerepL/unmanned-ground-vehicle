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

import numpy as np
import cv2 as cv
from common import anorm, getsize


class findObj():
    '''Classe que encontra informacoes sobre a localizacao de uim objeto'''
    def init_feature(self, name):
        FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
        FLANN_INDEX_LSH    = 6
        '''Inicializa a classe quanto aos argumentos'''
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
                flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            else:
                flann_params= dict(algorithm = FLANN_INDEX_LSH,
                                table_number = 6, # 12
                                key_size = 12,     # 20
                                multi_probe_level = 1) #2
            matcher = cv.FlannBasedMatcher(flann_params, {})  # bug : need to pass empty dict (#1329)
        else:
            matcher = cv.BFMatcher(norm)
        return detector, matcher


    def filter_matches(self, kp1, kp2, matches, ratio = 0.75):
        '''Aplica filtros para localizacao'''
        mkp1, mkp2 = [], []
        for m in matches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                m = m[0]
                mkp1.append( kp1[m.queryIdx] )
                mkp2.append( kp2[m.trainIdx] )
        p1 = np.float32([kp.pt for kp in mkp1])
        p2 = np.float32([kp.pt for kp in mkp2])
        kp_pairs = zip(mkp1, mkp2)
        return p1, p2

    def extracao(self, img1, H = None):
        '''Extrai as coordenadas do objeto'''
        h1, w1 = img1.shape[:2]

        if H is not None:
            corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
            corners = np.int32( 
                cv.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0) 
            )
            limpo = corners
            limpoinfo = np.float32([[0, 0], [0, 0]])
            limpoinfo = np.int32([[0, 0], [0, 0]])
            limpo[0][0] = limpo[0][0] - w1
            limpo[1][0] = limpo[1][0] - w1
            limpo[2][0] = limpo[2][0] - w1
            limpo[3][0] = limpo[3][0] - w1
            limpoinfo[0][0] = limpo[0][0] + 8
            limpoinfo[0][1] = limpo[0][1] + 16
            limpoinfo[1][0] = limpo[2][0] - 8
            limpoinfo[1][1] = limpo[2][1] - 16

        return limpo, limpoinfo
        
