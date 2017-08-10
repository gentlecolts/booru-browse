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
	
	def updateSearch(self):
		"""add new search terms and update the view"""
		print("new search terms:", self.search.tagsAsString())
		try:
			#pass the client and new query to the tileView
			""""""
		except Exception as e:
			alert(self, str(e))
	
	def openImage(self, imagedic):
		"swap over to "
