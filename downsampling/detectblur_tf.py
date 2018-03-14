# USAGE
# python detect_blur.py --images images

# import the necessary packages
from imutils import paths
import os, sys
import argparse
import subprocess
import glob
import time
import cv2
from PIL import Image
import os.path
import numpy as np

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_32F).var()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
	help="focus measures that fall below this value will be considered 'blurry'")
ap.add_argument("-d", "--destination", required=True,
	help="directory to put images that have been cleared")
ap.add_argument("-c", "--compress", action='store_true',
	help="Compress images bzip2")
ap.add_argument("-g", "--compressg", action='store_true',
	help="Compress images using gzip")
ap.add_argument("-s", "--squeeze", action='store_true',
	help="Compress images using squeeze")
args = vars(ap.parse_args())
destination = args["destination"]#+'/.'

#Make output directory
if not os.path.isdir(destination): subprocess.call(["mkdir", destination])
#Creating input directory
if not os.path.isdir(args["images"]): subprocess.call(["mkdir", args["images"]])


iwait=0
timeout=60
while True:

	#filet = glob.glob(args["images"]+'/*.tiff')
	files = glob.glob(args["images"]+'/*.tiff')

	if not files:
		if iwait >= timeout:
			print("Python Script Timing Out... Ending Normally.")
			break
		time.sleep(2);iwait+=2
		#print("Nothing: "+files)
		continue
	timestart = time.clock()

	#sys.exit(0)

	# loop over the input images
	#for imagePath in paths.list_images(args["images"]):
	fcnt=0
	for ifile in files:
		# load the image, convert it to grayscale, and compute the
		# focus measure of the image using the Variance of Laplacian
		# method
		try:
			image = cv2.imread(ifile,-1)
			print(image.dtype)
			print(image.shape)
		except:
			cmd = ["mv",ifile,destination]
			subprocess.call(cmd)
			continue
			
		#cv2.imshow('16bit TIFF', image)
		#cv2.waitKey()
		#print(image.dtype)
		#print(image.shape)
		#sys.exit(0)

		gray = image
		#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		fm = variance_of_laplacian(gray)

		#if True:
		#	cmd=["mv",ifile,destination+"/image0"+str(fcnt)+".png"]
		#	subprocess.call(cmd)
		if fm < args["threshold"]:
			cmd = ["rm","-rf",ifile]
			subprocess.call(cmd)
			print("DELETING - fm = "+str(fm))
		else:
			if args["compress"]:
				cmd = ["bzip2",ifile]
				subprocess.call(cmd)
				ifile = ifile+".bz2"
			if args["compressg"]:
				cmd = ["gzip",ifile]
				subprocess.call(cmd)
				ifile = ifile+".gz"
                        #./sz -z -f -c ../sz.config -i 1522.tiff -2 1200 1200
			if args["squeeze"]:
				cmd = ["./sz","-z","-f","-c","../sz.config","-i",ifile,"-2","1200","1200"]
				subprocess.call(cmd)
				ifile = ifile+".sz"
			cmd = ["mv",ifile,destination]
			subprocess.call(cmd)

		fcnt+=1

		"""
		text = "Not Blurry"
		# if the focus measure is less than the supplied threshold,
		# then the image should be considered "blurry"
		if fm < args["threshold"]:
			text = "Blurry"
			#print "this is the threshold: ", fm
		# show the image
		cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
		cv2.imshow("Image", image)
		#key = cv2.waitKey(0)
		"""

	timetrans = time.clock() - timestart
	print("Processed "+str(fcnt)+" files in "+str(timetrans)+" seconds")
