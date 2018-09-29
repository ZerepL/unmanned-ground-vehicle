import camera
import cv2 as cv

cam = camera
picExt = cam.tirafoto()
cv.imshow('image', picExt)
cv.waitKey(0)
cv.destroyAllWindows()