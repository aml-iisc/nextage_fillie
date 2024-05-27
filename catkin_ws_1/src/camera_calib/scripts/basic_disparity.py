import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
 
imgL = cv.imread('trash/imageL8.png', cv.IMREAD_GRAYSCALE)
imgR = cv.imread('trash/imageR8.png', cv.IMREAD_GRAYSCALE)
 
stereo = cv.StereoBM_create(numDisparities=64, blockSize=5)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.show()