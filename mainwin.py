import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from booruSearch import searchWidget
from tileView import tileView
from postView import postView
from errorReport import alert

class booruView(Gtk.Box):
	"""Viewer for boorus"""
	def __init__(self):
		"""set everything up"""
		super(booruView, self).__init__(orientation=Gtk.Orientation.VERTICAL)
		
		self.search=searchWidget(self)
		self.pack_start(self.search, expand=False, fill=True, padding=0)
		
		self.postPreview=tileView(self)
		self.pack_start(self.postPreview, expand=True, fill=True, padding=0)
		
		self.post=postView(self)
		self.pack_start(self.post, expand=True, fill=True, padding=0)
		self.post.set_no_show_all(True)
		self.post.hide()
		
		self.floater=Gtk.Window()
		self.floater.resize(1280, 720)
		def closeFloat(w, e):
			self.floater.hide()
			self.search.single.set_active(True)
			return True
		self.floater.connect('delete-event', closeFloat)
		self.floater.set_title("Post View")
		
		self.show_all()
		self.setSingleWin(False)
		
		self.currentPost=None
	
	def updateSearch(self):
		"""add new search terms and update the view"""
		query=self.search.tagsAsString()
		#print("new search terms: ", query)
		client=self.search.getClient()
		if client and query:
			#try:
				self.postPreview.updateSearch(self.search.getClient(), query)
			#except Exception as e:
			#	print(e)
			#	alert(self, str(e))
	
	def openImage(self, imagedic, reload=True):
		#from pprint import pprint
		#pprint(imagedic)
		
		self.currentPost=imagedic
		
		if 'artist' in imagedic:
			self.floater.set_title("Post View - {}".format(" ".join(imagedic['artist'])))
			#self.floater.set_title("Post View -\t{}\t- {}".format(" ".join(imagedic['artist']), imagedic['tags']))
		else:
			self.floater.set_title("Post View")
		
		if reload:
			self.post.load(imagedic)
		
		if self.single:
			self.postPreview.set_no_show_all(True)
			self.postPreview.hide()
			self.post.set_no_show_all(False)
			self.post.show()
	
	def next(self, jump=1):
		#TODO: should be able to go across pages
		#TODO: visual indication of the currently loaded post (should probably go in openImage)
		page=self.postPreview.results
		try:
			pindex=page.index(self.currentPost)
		except ValueError:
			print("probably dont have anything selected, cant call next")
			return
		
		#python allowing this syntax is rediculous, but since it does, may as well make use of
		if 0<=pindex+jump<len(page):
			self.openImage(page[pindex+jump])
	
	def closeImage(self):
		self.post.set_no_show_all(True)
		self.post.hide()
		self.postPreview.set_no_show_all(False)
		self.postPreview.show()
	
	def setSingleWin(self, single):
		print("single win set to: "+str(single))
		self.single=single
		
		if single:
			#hide the floating window
			self.floater.hide()
			
			#remove media from floating window and the toolbar from self
			self.floater.remove(self.post.media)
			self.remove(self.post.toolbar)
			
			#and put that media back in the post widget
			self.post.addMedia()
		else:
			#go back to tile view if we're not in it
			self.closeImage()
			
			#remove media from the post view
			self.post.removeMedia()
			
			#put the toolbar in self
			self.add(self.post.toolbar)
			self.reorder_child(self.post.toolbar, 1)
			#self.show_all()
			
			#put the media in the floating window
			self.floater.add(self.post.media)
			#self.floater.show_all()
			self.floater.show()
			
