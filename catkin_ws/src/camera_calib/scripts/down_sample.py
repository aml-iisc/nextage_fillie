import cv2 as cv
import glob
import os

def downsample_image(image, reduce_factor):
	for i in range(0,reduce_factor):
		#Check if image is color or grayscale
		print(image.shape)
		if len(image.shape) > 2:
			row,col = image.shape[:2]
		else:
			row,col = image.shape
		# print(row,col)
		image = cv.pyrDown(image, dstsize= (col//2, row // 2))
	return image


imagesLeft = sorted(glob.glob('images/stereoLeft/*.png'))
imagesRight = sorted(glob.glob('images/stereoRight/*.png'))

# imagesLeft = sorted(glob.glob('trash/2/L/*.png'))
# imagesRight = sorted(glob.glob('trash/2/R/*.png'))

print(len(imagesLeft))

filesl = glob.glob('down_images/stereoLeft/*')
filesr = glob.glob('down_images/stereoRight/*')
for fl,fr in zip(filesl,filesr):
    os.remove(fl)
    os.remove(fr)

num=0
for imgLeft, imgRight in zip(imagesLeft, imagesRight):
    imgL = cv.imread(imgLeft)
    imgR = cv.imread(imgRight)
    dl=downsample_image(imgL,1)
    dr=downsample_image(imgR,1)
    print(dl.shape,dr.shape)
    cv.imwrite('down_images/stereoLeft/imageL' + str(num) + '.png', dl)
    cv.imwrite('down_images/stereoRight/imageR' + str(num) + '.png', dr)
    num= num +1