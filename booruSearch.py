import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class taglabel(Gtk.Box):
	def __init__(self, owner):
		super(taglabel, self).__init__(orientation=Gtk.Orientation.HORIZONTAL)

class booruLister(Gtk.ComboBoxText):
	def __init__(self):
		super(taglabel, self).__init__()

class searchWidget(Gtk.Box):
	"""search bar"""
	def __init__(self, booruWidget):
		"""set everything up"""
		super(searchWidget, self).__init__(orientation=Gtk.Orientation.VERTICAL)
		
