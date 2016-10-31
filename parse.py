#!C:\dev\interpreter\python\python.exe
#
#######################################################
# Python script for parsing exif2.2 values from jpegs #
#######################################################
#
#

import dircache
import os
import EXIF
import re
import datetime

#class exif:
#	def __init__(self, path="."):
#		self.path = path
#		for i in sys.argv:
#			print i
		
dic=[]

class Fore:
	IMGlist = []
	def __init__(self):
		return


	def getdate(self,filename):
		imagefile = file(filename,"rb")
		imagetags = EXIF.process_file(imagefile)
		imagefile.close()
#		print dir(imagetags['EXIF DateTimeOriginal'])
#		return imagetags['EXIF DateTimeOriginal']
		datestr = imagetags['EXIF DateTimeOriginal']
		datelist = re.search(r'(....):(..):(..) (..):(..):(..).*',datestr.printable).group
		date = datetime.datetime(int(datelist(1)),int(datelist(2)), int(datelist(3)), int(datelist(4)), int(datelist(5)), int(datelist(6)))
		return date


		


	def formatdate(self,adate, formstring):
######################################################################################		
#		le = re.compile(r'(....):(..):(..) (..):(..):(..).*')                #
#		print type(adate)                                                    #
#		print adate.__class__                                                #
#		print le.sub(r'\3-\4.\5.\6',adate)                                   #
#		return le.sub(r'\3-\4.\5.\6',adate) #re.sub(,r'\1-\2-\3-\4',adate)   #
######################################################################################

#		bdate = datetime.timedelta(0,0,0,0,16,1)			# DELTA OPERATIONS
#		adate += bdate
		return formstring #% {"year":adate.year,"month":adate.month}              # FIX DAS HIELR!!!!!!!!!!!!!!!!!!1

	def addimages(self, dir="."):
		j = 0
		dl = os.listdir(dir)
		print dl
		dic=[]
		for i in dl:
			if i.lower().endswith(".jpg"):
#				self.IMGlist.append([dir+"/"+i,self.cleandate(self.getdate(dir+"\\"+i))])
				self.IMGlist.append([dir+"/"+i,self.getdate(dir+"/"+i)])
		for i in self.IMGlist:
			print i
		return dic

	def removedoubled(self, mydic):
		for i in range(0,len(mydic)):
			j=0
			for k in range(i+1, len(mydic)):
				if mydic[i][1] == mydic[k][1]:
					j += 1
					mydic[k][1] = "{1} ({0})".format(j, mydic[k][1])
			if j != 0:
				mydic[i][1] = "{1} ({0})".format(0, mydic[i][1])
		return (mydic)
	

#dic = parseimages()
#dic2 = removedoubled(dic)

#for i in dic2:
#	os.rename(i[0],"{0}.jpg".format(i[1]))










