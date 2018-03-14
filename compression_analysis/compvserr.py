# compressionTester.py
# 
# Script to compare the performance of gzip, bzip, and sz 
# compression for applications in streaming workflows.
# *Raw files are included for quick calculation
# If raw files are deleted, depending on the number set on ntrials,
# it can take up to 10 minutes to run, to get an overall average.
# 
# Use: (1) Create images/ directory with one or more *.tiff images
#      (2) python compressionTester.py 
#

from imutils import paths
import os, sys
import argparse
import subprocess
import glob
import time
import cv2
#from PIL import Image
import os.path
import numpy as np
import math
import matplotlib.pyplot as plt

ntrials=10
use_saved=True # Use saved data if its available
styleuse = 'ggplot'
plt.style.use(styleuse)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", default="images", help="path to input image")
#ap.add_argument("-s", "--squeeze", action='store_true',
#	help="Compress images using squeeze")
args = vars(ap.parse_args())
#f, ax = plt.subplots(1, 2, figsize=(12, 6))
f1, ax1 = plt.subplots(1, 1, figsize=(6, 6))
f2, ax2 = plt.subplots(1, 1, figsize=(6, 6))
ax = [ax1, ax2]

files = glob.glob(args["image"]+"/*.tiff")
for ifile in files:

	for c_alg in ["sz", "bzip2", "gzip"]:

		try:
			image = cv2.imread(ifile,-1)
			image = image.astype("float32")
			print(image.dtype)
			print(image.shape)
			dtype = image.dtype
			(x1, x2) = image.shape
		except:
			print("Error -- Couldnt open the file!!")
			#sys.exit(-1)

		statinfo = os.stat(ifile)
		orig_size = float(statinfo.st_size)
		print("originale size: "+str(statinfo.st_size))

		RATIO = []
		TIME_AVG = []
		TIME_STD = []
		ERR_list = [1E-6,1E-5,1E-4,1E-3,1E-2,1E-1,1E0]
		for err in ERR_list:

			time_vec=[]
			comp_size=1.0
			try:
				if c_alg =="sz":
					cmd = ["./sz","-z","-f","-i",ifile,"-M","ABS","-A",str(err),"-2",str(x1),str(x2)]
					cfile = ifile+".sz"
				elif c_alg =="bzip2":
					cmd = ["bzip2",ifile]
					cfile = ifile+".bz2"
				elif c_alg =="gzip":
					cmd = ["gzip",ifile]
					cfile = ifile+".gz"

				# Error bound wont change result... continue...
				if c_alg != "sz" and err != ERR_list[0]:
					RATIO.append(RATIO[-1])
					TIME_AVG.append(TIME_AVG[-1])
					TIME_STD.append(TIME_STD[-1])
					continue

				#rawfile=str(c_alg)+'_'+str(err)+'.raw'
				rawfile=str(c_alg)+'_'+str(err)+'_'+os.path.basename(ifile)+'.raw'
				if os.path.isfile(rawfile) and use_saved:
					print("YES "+rawfile)
					fh = open(rawfile, 'r')
					while True:
						line = fh.readline()
						if not line: break
						fsplt = line.split()
						timecomp = float(fsplt[0])
						comp_size = float(fsplt[1])
						time_vec.append(timecomp)
					fh.close()

				else:
					print("NO "+rawfile)
					fh = open(rawfile, 'a')
					for itrial in range(ntrials):
						timestart = time.clock()
						subprocess.call(cmd)
						timecomp = time.clock() - timestart
						statinfo = os.stat(cfile)
						comp_size = float(statinfo.st_size)
						if c_alg =="sz": subprocess.call(["rm",cfile])
						elif c_alg =="bzip2": subprocess.call(["bzip2","-d",cfile])
						elif c_alg =="gzip": subprocess.call(["gunzip",cfile])
						time_vec.append(timecomp)
						fh.write("%f %f\n" %(timecomp, comp_size))
					fh.close()

			except:
				print("Error -- Couldnt COMPRESS the file!!")
				continue #sys.exit(-1)

			#comp_size = float(statinfo.st_size)
			print("RATIO: "+str(orig_size / comp_size))
			RATIO.append( orig_size / comp_size )
			timecomp=np.mean(time_vec)
			print("TIME: "+str(timecomp))
			TIME_AVG.append( timecomp )
			TIME_STD.append( np.std(time_vec) / math.sqrt(ntrials) )
			#if c_alg =="sz":
			#	subprocess.call(["rm",cfile])
			#elif c_alg =="bzip2":
			#	subprocess.call(["bzip2","-d",cfile])
			#elif c_alg =="gzip":
			#	subprocess.call(["gunzip",cfile])

		#Decompress
		#cmd = ["./sz","-x","-f","-s",cfile,"-2",str(x1),str(x2)]
		#subprocess.call(cmd)

		if len(RATIO) > 0:
			ax[0].plot(ERR_list,RATIO,'-o',label='56MiB-'+c_alg)
			#ax[0].set_yscale('log')
			ax[0].set_xscale('log')

			ax[1].errorbar(ERR_list,TIME_AVG,yerr=TIME_STD,fmt='-o',capsize=3,label='56MiB-'+c_alg)
			ax[1].set_xscale('log')

ax[0].set_title('Compression Ratio vs Error')
ax[0].set_xlabel('Absolute Error Bound')
ax[0].set_ylabel('Compression Ratio')
ax[0].legend(loc='best')

ax[1].set_title('Compression Time vs Error')
ax[1].set_xlabel('Absolute Error Bound')
ax[1].set_ylabel('Time [sec]')

#plt.subplots_adjust(left=0.07, bottom=None, right=0.97, top=None, wspace=0.26, hspace=None)
#f.savefig('yplot.png', dpi=100)
f1.subplots_adjust(left=0.15, bottom=0.12, right=0.94, top=0.92, wspace=None, hspace=None)
f2.subplots_adjust(left=0.17, bottom=0.12, right=0.94, top=0.92, wspace=None, hspace=None)
f1.savefig('yplot1.png', dpi=100)
f2.savefig('yplot2.png', dpi=100)
plt.show()
