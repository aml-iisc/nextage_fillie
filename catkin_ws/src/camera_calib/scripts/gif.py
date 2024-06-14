import imageio.v3 as iio

filenames = ['images/stereoLeft/imageL'+str(num)+'.png' for num in range(10,459)]

images = [ ]

for filename in filenames:
  images.append(iio.imread(filename))
print(len(images))
iio.imwrite('full.mp4', images,fps=30)

