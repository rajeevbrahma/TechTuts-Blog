import cv2
import imutils
import sys
import numpy as np
from matplotlib import pyplot as plt

from imutils.perspective import four_point_transform
from imutils import contours


import random


def main():

	ANSWER_KEY = {}

	ANSWER_KEY = {0:1,1:1,2:2,3:3,4:4,5:3,6:2,7:1,8:0,9:1,10:2,11:3,12:4,13:3,14:2,15:1,16:0,17:1,18:2,19:3,20:4,21:3,22:2,23:1,24:0,25:1}


	# for key in range(0,24):
	# 	ANSWER_KEY.update({key:random.randint(0,4)})

	print ANSWER_KEY

	image = cv2.imread(sys.argv[1])
	grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	plt.imshow(grey)
	# plt.show()
	blurred = cv2.GaussianBlur(grey, (5,5),0)
	plt.imshow(blurred)
	plt.show()
	edged = cv2.Canny(blurred,75,200)	


	

	#  binarizing the image to segregate the foreground with the background
	#  we are using a otsu thresholding method to binarize the warped
	thresh = cv2.threshold(edged.copy(), 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	plt.imshow(thresh)
	plt.show()	

	cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)	
	cnts = imutils.grab_contours(cnts)	
	questionCnts = []
	# print cnts
	for c in cnts:
		(x,y,w,h) = cv2.boundingRect(c)
		ar = w/float(h)
		
		# print ("AR=%f,x=%d,Y=%d,W=%d,H=%d"%(ar,x,y,w,h))
		# print "\n"

		
		if 47<=w<=50 and 47<=h<=50 and ar>=0.9 and ar<=1.2:
			questionCnts.append(c)



	print len(questionCnts)

		
	questionCnts = contours.sort_contours(questionCnts,method="top-to-bottom")[0]
	correct = 0	
	
	
	# for v in range(0,len(questionCnts)):
	# 	bubbl = cv2.drawContours(image,[questionCnts[v]],-1,255,-1)
	# 	print "=====\n"
	# 	print questionCnts[v]	
	# 	print "\n====="
 		
	# 	plt.imshow(bubbl)
	# 	plt.show()


	

	for (q,i) in enumerate(np.arange(0,len(questionCnts),5)):
		# print "=====\n"
		# print q,i	
		# print "\n====="
		cnts = contours.sort_contours(questionCnts[i:i+5])[0]
		

		bubbled = None
		for (j,c) in enumerate(cnts):

			# (x,y,w,h) = cv2.boundingRect(c)
			# ar = w/float(h)
			
			# print ("AR=%f,x=%d,Y=%d,W=%d,H=%d"%(ar,x,y,w,h))
			# print "\n"

			


			# mask = np.zeros(edged.shape,dtype="uint8")
			# bubbl = cv2.drawContours(mask,[c],-1,255,-1)		
			# mask = cv2.bitwise_and(edged,edged,mask=mask)


			#  ---------------- taking binary image -------
			mask = np.zeros(thresh.shape,dtype="uint8")
			bubbl = cv2.drawContours(mask,[c],-1,255,-1)		
			mask = cv2.bitwise_and(thresh,thresh,mask=mask)

			# bubb = cv2.drawContours(image,[c],-1,255,-1)

			# plt.imshow(bubb)
			# plt.show()

			total = cv2.countNonZero(mask)
			# print "\t+++\n\t\t"
			# print total
			# print "\n\t+++"
			
			if(bubbled is None or total>bubbled[0]):
				bubbled = (total,j)
				print bubbled,"BUBBLED"



		color = (255,0,0)
		k = ANSWER_KEY[q]
		# print "\t+++\n\t\t"
		# print k,q,bubbled[1]			
		# print "\n\t+++"	
		if k == bubbled[1]:
			# print "\t+++\n\t\t"
			# print k, bubbled[1]			
			# print "\n\t+++"	

			color = (0,255,0)
			correct +=1

		bubbl2 = cv2.drawContours(image,[cnts[k]],-1,color,3)
		plt.imshow(bubbl2)
		plt.show()



if __name__ == '__main__':
	main()


	