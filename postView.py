import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class postView(Gtk.HBox):
	"""settings and stuff"""
	def __init__(self, booruWidget):
		"""set everything up"""
		super(postView, self).__init__()
		
