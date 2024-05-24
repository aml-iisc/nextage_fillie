import numpy as np
import cv2 as cv
import glob
from matplotlib import pyplot as plt

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

chessboardSize = (9,6)
# chessboardSize = (6,4)
# frameSize = (484,274)
# frameSize = (1936,1096)
frameSize = (968,548)
# ratio = float(1936.0)/1096.0
# # print(ratio)
# width = int(480*ratio)
# frameSize = (width, 480)


# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

print(objp)
# objp = objp * 0.108
objp = objp * 0.02
#print(objp)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpointsL = [] # 2d points in image plane.
imgpointsR = [] # 2d points in image plane.


imagesLeft = sorted(glob.glob('images/stereoLeft/*.png'))
imagesRight = sorted(glob.glob('images/stereoRight/*.png'))

# imagesLeft = sorted(glob.glob('trash/1/L/*.png'))
# imagesRight = sorted(glob.glob('trash/1/R/*.png'))



# imagesLeft = sorted(glob.glob('down_images/stereoLeft/*.png'))
# imagesRight = sorted(glob.glob('down_images/stereoRight/*.png'))

for imgLeft, imgRight in zip(imagesLeft, imagesRight):
    # print("hii")

    imgL = cv.imread(imgLeft)
    imgR = cv.imread(imgRight)
    # imSL = cv.resize(imgL, (width, 480))
    # imSR = cv.resize(imgR, (width, 480))
    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    retL, cornersL = cv.findChessboardCorners(grayL, chessboardSize, None)
    retR, cornersR = cv.findChessboardCorners(grayR, chessboardSize, None)

    # If found, add object points, image points (after refining them)
    if retL and retR == True:

        objpoints.append([objp,imgLeft,imgRight])

        cornersL = cv.cornerSubPix(grayL, cornersL, (11,11), (-1,-1), criteria)
        imgpointsL.append(cornersL)

        cornersR = cv.cornerSubPix(grayR, cornersR, (11,11), (-1,-1), criteria)
        imgpointsR.append(cornersR)

        # Draw and display the corners
        cv.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
        cv.imshow('img left', imgL)
        cv.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
        cv.imshow('img right', imgR)
        cv.waitKey(500)


cv.destroyAllWindows()




############## CALIBRATION #######################################################

objm = [i[0] for i in objpoints]

retL, cameraMatrixL, distL, rvecsL, tvecsL = cv.calibrateCamera(objm, imgpointsL, frameSize, None, None,flags=cv.CALIB_FIX_K1 or cv.CALIB_FIX_K2 or cv.CALIB_FIX_K3 or cv.CALIB_FIX_K4 or cv.CALIB_FIX_K5 or cv.CALIB_FIX_K6 or cv.CALIB_FIX_PRINCIPAL_POINT)
heightL, widthL, channelsL = imgL.shape
newCameraMatrixL, roi_L = cv.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

retR, cameraMatrixR, distR, rvecsR, tvecsR = cv.calibrateCamera(objm, imgpointsR, frameSize, None, None,flags=cv.CALIB_FIX_K1 or cv.CALIB_FIX_K2 or cv.CALIB_FIX_K3 or cv.CALIB_FIX_K4 or cv.CALIB_FIX_K5 or cv.CALIB_FIX_K6 or cv.CALIB_FIX_PRINCIPAL_POINT)
heightR, widthR, channelsR = imgR.shape
newCameraMatrixR, roi_R = cv.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))

# print(cameraMatrixL)
# print(newCameraMatrixL)

mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i][0], rvecsL[i], tvecsL[i], newCameraMatrixL, distL)
    error = cv.norm(imgpointsL[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    # print(i,error,objpoints[i][1],objpoints[i][2])
    mean_error += error


print("total error left: {}".format(mean_error/len(objpoints)))

mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i][0], rvecsR[i], tvecsR[i], newCameraMatrixR, distR)
    error = cv.norm(imgpointsR[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    # print(i,error,objpoints[i][1],objpoints[i][2])
    mean_error += error


print("total error right: {}".format(mean_error/len(objpoints)))

########## Stereo Vision Calibration #############################################

flags=0
flags |= cv.CALIB_FIX_INTRINSIC
# flags |= cv.CALIB_RATIONAL_MODEL
# flags |= cv.CALIB_FIX_PRINCIPAL_POINT
# flags |= cv.CALIB_USE_INTRINSIC_GUESS
# flags |= cv.CALIB_FIX_FOCAL_LENGTH
# flags |= cv.CALIB_FIX_ASPECT_RATIO
# flags |= cv.CALIB_ZERO_TANGENT_DIST

# print(newCameraMatrixL)

# flags = 0
# flags |= cv.CALIB_FIX_INTRINSIC
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same 




criteria_stereo = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(objm, imgpointsL, imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], criteria_stereo, flags=flags)


# print(trans)
# trans = np.array([[-0.1368163173523564], [-0.0010205012356274434], [0.01668293589994927]])

# Reprojection Error
mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i][0], rvecsL[i], tvecsL[i], newCameraMatrixL, distL)
    error = cv.norm(imgpointsL[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    print(i,error,objpoints[i][1],objpoints[i][2])
    mean_error += error


print("total error: {}".format(mean_error/len(objpoints)))



########## Stereo Rectification #################################################
# print("rot",rot,"trans",trans)
rectifyScale= 1
rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R= cv.stereoRectify(newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], rot, trans, rectifyScale,(0,0))
print(Q)
# print("hii")
# projMatrixR[0][3]= projMatrixR[0][3]//100 
# print(newCameraMatrixL,newCameraMatrixR,rectL,rectR,distL,distR,"projl",projMatrixL,"projR",projMatrixR)

stereoMapL = cv.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv.CV_16SC2)
stereoMapR = cv.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv.CV_16SC2)

print("Saving parameters!")
cv_file = cv.FileStorage('stereoMap.xml', cv.FILE_STORAGE_WRITE)

cv_file.write('stereoMapL_x',stereoMapL[0])
cv_file.write('stereoMapL_y',stereoMapL[1])
cv_file.write('stereoMapR_x',stereoMapR[0])
cv_file.write('stereoMapR_y',stereoMapR[1])
cv_file.write('q', Q)

cv_file.release()