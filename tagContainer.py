import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class taglabel(Gtk.Box):
	def __init__(self, owner):
		super(taglabel, self).__init__(orientation=Gtk.Orientation.HORIZONTAL)

class tagBox(Gtk.Grid):
	def __init__(self, owner):
		super(tagBox, self).__init__()
		
		self.taglist={}
	
	def addTags(self, tags):
		"add tags"
	
	def removeTag(self, tag):
		"remove tag"
	
	def clear(self):
		"remove all tags"
