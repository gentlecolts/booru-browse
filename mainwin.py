import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from booruSearch import searchWidget
from tileView import tileView
from postView import postView

class booruView(Gtk.Box):
	"""Viewer for boorus"""
	def __init__(self, booruClient):
		"""set everything up"""
		super(booruView, self).__init__(orientation=Gtk.Orientation.VERTICAL)
		
		self.client=booruClient
		
		self.search=searchWidget(self)
		self.pack_start(self.search, expand=False, fill=True, padding=0)
		
		self.postPreview=tileView(self)
		self.pack_start(self.postPreview, expand=True, fill=True, padding=0)
		
		self.post=postView(self)
	
	def updateSearch(self, newtags):
		"""add new search terms and update the view"""
