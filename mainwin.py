import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

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
	
	def updateSearch(self):
		"""add new search terms and update the view"""
		query=self.search.tagsAsString()
		#print("new search terms: ", query)
		client=self.search.getClient()
		if client and query:
			try:
				self.postPreview.updateSearch(self.search.getClient(), query)
			except Exception as e:
				print(e)
				alert(self, str(e))
	
	def openImage(self, imagedic):
		#TODO:swap out the tiles with the post itself
		from pprint import pprint
		pprint(imagedic)
		
		self.post.load(imagedic)
		
		self.postPreview.set_no_show_all(True)
		self.postPreview.hide()
		self.post.set_no_show_all(False)
		self.post.show()
	
	def closeImage(self):
		self.post.set_no_show_all(True)
		self.post.hide()
		self.postPreview.set_no_show_all(False)
		self.postPreview.show()
