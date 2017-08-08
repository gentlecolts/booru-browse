import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class settingWidget(Gtk.Box):
	"""settings and stuff"""
	def __init__(self, booruWidget):
		"""set everything up"""
		super(settingWidget, self).__init__(orientation=Gtk.Orientation.VERTICAL)
		
		
