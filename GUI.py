#!c:/Python27/python.exe

import wx, os, parse, dircache, shutil
import EXIF, re, datetime, thread

class MainFrame(wx.Frame):

	def __init__(self, parent, title, size):
		wx.Frame.__init__(self, parent, title=title, size=size)
		self.CreateStatusBar() # Creates weird Statusbar in bottom

		self.dirlist = []
		self.outputdir = ""
#		self.fore = parse.Fore()
		self.previewstring = "Preview: "
		self.processed = 0
		self.IMGlist = []

		# Setting up the menu
		filemenu=wx.Menu()
		helpmenu=wx.Menu()

		# wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets
		menuAbout = helpmenu.Append(wx.ID_ABOUT, "&About", "Blabla")
		menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Quit")


		#creating the menubar
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File") # Add "filemenu" to the MenuBar
		menuBar.Append(helpmenu, "&Help")
		self.SetMenuBar(menuBar) # Add "menuBar" to the Frame content

		# Set Events
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

		# O/I Directories
		# Create Sizer Enviroments
		self.IOsizerMAIN = wx.BoxSizer(wx.VERTICAL)
		self.IOsizerBTN1 = wx.BoxSizer(wx.HORIZONTAL)
		self.IOsizerBTN1sub = wx.BoxSizer(wx.VERTICAL)
		self.IOsizerBTN2 = wx.BoxSizer(wx.HORIZONTAL)
		# Define Content for Sizer Enviroments
		self.textid = wx.StaticText(self, label="Input Directories")
		self.inputid = wx.ListBox(self, size=(200,60))
		self.textod = wx.StaticText(self, label="Output Directory")
		self.inputod = wx.TextCtrl(self, size=(200,-1))
		self.textfs = wx.StaticText(self, label="Format String")
		self.inputfs = wx.TextCtrl(self, size=(200,-1))
		self.prevfs = wx.StaticText(self, label="Preview: ")
		self.progressbar = wx.Gauge(self, wx.GA_HORIZONTAL, size=(600,30))


		self.BTNadddir = wx.Button(self,1,"&Add")
		self.BTNremdir = wx.Button(self,2,"&Remove")
		self.BTNoutdir = wx.Button(self,3,"&Output")

		#Bind Events
		self.Bind(wx.EVT_BUTTON, self.OnAdd, self.BTNadddir)
		self.Bind(wx.EVT_BUTTON, self.OnRemove, self.BTNremdir)
		self.Bind(wx.EVT_BUTTON, self.OnOutput, self.BTNoutdir)
		self.Bind(wx.EVT_TEXT, self.OnTypingFP, self.inputfs)

		# Add Content to Sizer Enviroments
		self.IOsizerBTN1.Add(self.inputid,0)
		self.IOsizerBTN1sub.Add(self.BTNadddir,0)
		self.IOsizerBTN1sub.Add(self.BTNremdir,0)
		self.BTNremdir.Disable()
		self.IOsizerBTN1.Add(self.IOsizerBTN1sub,0)
		self.IOsizerBTN2.Add(self.inputod,0)
		self.IOsizerBTN2.Add(self.BTNoutdir,0)
		# Add Subsizer to Mainsizer
		self.IOsizerMAIN.Add(self.textid,0)
		self.IOsizerMAIN.Add(self.IOsizerBTN1,0)
		self.IOsizerMAIN.Add(self.textod,0)
		self.IOsizerMAIN.Add(self.IOsizerBTN2,0)
		# Add Formatpreview to MainSizer
		self.IOsizerMAIN.Add(self.textfs,0)
		self.IOsizerMAIN.Add(self.inputfs,0)
		self.IOsizerMAIN.Add(self.prevfs,0)



		# Process Button
		self.sizerbottom = wx.BoxSizer(wx.VERTICAL)
		self.BTNStart = wx.Button(self,4,"&Process")
		self.BTNStart.Disable()
		self.Bind(wx.EVT_BUTTON,self.OnProcess,self.BTNStart)
		self.sizerbottom.Add(self.BTNStart, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT)
		self.IOsizerMAIN.Add(self.sizerbottom, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT)
		self.IOsizerMAIN.Add(self.progressbar)



		#Layout sizers
		self.SetSizer(self.IOsizerMAIN)
		self.SetAutoLayout(1)
		self.Show()

		self.Show(True)

	def OnAdd(self, e):
		print e
		""" Add Inputdirectory """
		dialog = wx.DirDialog(self, "Choose a directory")
		if dialog.ShowModal() == wx.ID_OK:
			if dialog.GetPath() not in self.dirlist:
				self.dirlist.append(dialog.GetPath())
			self.inputid.Set(self.dirlist)
			self.BTNremdir.Enable()
			self.BTNStart.Enable()

	def OnOutput(self, e):
		""" Ahh Outputdirectry """
		dialog = wx.DirDialog(self, "Choose a directory")
		if dialog.ShowModal() == wx.ID_OK:
			self.outputdir = dialog.GetPath()
		self.inputod.Clear()
		print self.outputdir
		self.inputod.WriteText(self.outputdir)
		dialog.Destroy()

	def OnRemove(self, e):
		""" Remove Inputdiretory """
		self.dirlist.pop(self.inputid.GetSelection())
		self.inputid.Set(self.dirlist)
		if (len(self.dirlist) == 0):
			self.BTNremdir.Disable()
			self.BTNStart.Disable()


	def OnAbout(self, e):
		"""  About Window """
		info = wx.AboutDialogInfo()
		info.Name = "Fore"
		info.Version = "0.3"
		info.Copyright = "(C) 2002 Roman Bruckner"
		info.Description = "A sophisticated foto renaming tool"
		info.WebSite = ("http://www.romanbr.de/", "Official Website")
#		info.Developers = ["Roman Bruckner"]
		wx.AboutBox(info)

	def OnExit(self, e):
		self.Close(True)

#	def OnInput(self,e):
#		""" Open a file"""
#		self.dirname = ''
#		dlg = wx.DirDialog(self, "Choose a file")
#		if dlg.ShowModal() == wx.ID_OK:
#			self.filename = dlg.GetFilename()
#			self.dirname = dlg.GetDirectory()
#			print self.filename
#			print self.dirname
#		else:
#			print "ABORT"
#		dlg.Destroy()

	def OnProcess(self, e):
#               COPYING FILES
		if(self.processed):
			self.BTNadddir.Disable()
			self.BTNremdir.Disable()
			self.BTNStart.Disable()
			self.progressbar.SetValue(0)
			for i in self.IMGlist:
				i[1] = "{1}\\{0}".format(self.formatdate(i[1],self.inputfs.GetLineText(0)),self.outputdir)
			self.removedoubled(self.IMGlist)
			for i in self.IMGlist:
#                               os.rename(i[0],"{0}.jpg".format(i[1])) #RENAME
				print repr(os.path.dirname(i[1]))
				print os.path.dirname(i[1]).__class__()
				if not os.path.isdir(os.path.dirname(i[1])):
					os.mkdir(os.path.dirname(i[1]))
				shutil.copy2(i[0],"{0}.jpg".format(i[1])) #RENAME self.formatdate(self.IMGlist[0][1],self.inputfs.GetLineText(0))
#				shutil.copy2(i[0],i[1])
				print "%s -> %s" % (i[0],i[1])
			self.BTNadddir.Enable()
			self.BTNremdir.Enable()
			self.BTNStart.Enable()
			return
#               PROCESSING IMAGES
		thread.start_new_thread(self.addimages,())
		self.processed = 1
		self.BTNStart.SetLabel("Rename")


	def OnTypingFP(self, e):
		forbiddenchars = [":","*","?","\"","<",">","|"]
		text = self.inputfs.GetLineText(0)
		if self.processed and len(text) != 0:
			i = 0
			pos = self.inputfs.GetInsertionPoint()
			if text[pos-1] in forbiddenchars:
				self.inputfs.SetValue(text[0:pos-1]+text[pos:text.__len__()])
				self.inputfs.SetInsertionPoint(pos-1)
			else:
				self.prevfs.SetLabel("Preview: " + self.formatdate(self.IMGlist[0][1],self.inputfs.GetLineText(0)))


	# (ex)PARSE.py



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
		formlist = {}
		replacepos = []
		replacetype = []
		outputstr = ""
		j = 0
		for i in range(len(formstring)):
			if formstring[i] == "%":
				if i+1 < len(formstring):
					if formstring[i+1] == "Y":
						formlist["year"] = adate.year
						outputstr = outputstr + formstring[j:i] + "%(year)04d"
						j=i+2
					elif formstring[i+1] == "M":
						formlist["month"] = adate.month
						outputstr = outputstr + formstring[j:i] + "%(month)02d"
						j=i+2
					elif formstring[i+1] == "D":
						formlist["day"] = adate.day
						outputstr = outputstr + formstring[j:i] + "%(day)02d"
						j=i+2
					elif formstring[i+1] == "h":
						formlist["hour"] = adate.hour
						outputstr = outputstr + formstring[j:i] + "%(hour)02d"
						j=i+2
					elif formstring[i+1] == "m":
						formlist["minute"] = adate.minute
						outputstr = outputstr + formstring[j:i] + "%(minute)02d"
						j=i+2				
					elif formstring[i+1] == "s":
						formlist["second"] = adate. second
						outputstr = outputstr + formstring[j:i] + "%(second)02d"
						j=i+2
					else:
						outputstr = outputstr + formstring[j:i] + "%%"
						j=i+1
				else:
					outputstr = outputstr + formstring[j:i] + "%%"
					j=i+1
					
		outputstr = outputstr + formstring[j:len(formstring)]
		return outputstr % formlist

	def addimages(self):
		self.BTNadddir.Disable()
		self.BTNremdir.Disable()
		self.BTNStart.Disable()
		self.progressbar.SetValue(0)
		nfiles = 0
		dl = []
		for i in self.dirlist:
			k = [i,os.listdir(i)]
			dl.append(k)
			nfiles += len(k[1])
		self.progressbar.SetRange(nfiles)
		mfiles=0

		for j in dl:
			for i in j[1]:
				if i.lower().endswith(".jpg"):
#					self.IMGlist.append([dir+"/"+i,self.cleandate(self.getdate(dir+"\\"+i))])
					self.IMGlist.append([j[0]+"/"+i,self.getdate(j[0]+"/"+i)])
					mfiles+= 1
					self.progressbar.SetValue(mfiles)
					print nfiles, mfiles
		for i in self.IMGlist:
			print i

		self.BTNadddir.Enable()
		self.BTNremdir.Enable()
		self.BTNStart.Enable()


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


app = wx.App()
frame = MainFrame(None, 'Fore',(600,350))
app.MainLoop()

