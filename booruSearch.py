import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from tagContainer import tagBox

class booruLister(Gtk.ComboBoxText):
	def __init__(self):
		super(booruLister, self).__init__()

class searchWidget(Gtk.Box):
	"""search bar"""
	def __init__(self, booruWidget):
		"""set everything up"""
		super(searchWidget, self).__init__(orientation=Gtk.Orientation.VERTICAL)
		
		buttonRow=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		
		#search related buttons
		self.searchbar=Gtk.SearchEntry()
		buttonRow.pack_start(self.searchbar, expand=True, fill=True, padding=0)
		#TODO: attach event listeners
		
		searchbutton=Gtk.Button(label="Update Search")
		buttonRow.pack_start(searchbutton, expand=False, fill=True, padding=0)
		#TODO: attach event listeners
		
		resetbutton=Gtk.Button(label="Reset Search")
		buttonRow.pack_start(resetbutton, expand=False, fill=True, padding=0)
		#TODO: attach event listeners
		
		#some spacing
		spacer=Gtk.Fixed()
		buttonRow.pack_start(spacer, expand=True, fill=True, padding=0)
		
		#settings related buttons
		self.boorus=booruLister()
		buttonRow.pack_start(self.boorus, expand=False, fill=True, padding=0)
		#TODO: attach event listeners
		
		blocklister=Gtk.Button(label="Blocklist")
		buttonRow.pack_start(blocklister, expand=False, fill=True, padding=0)
		#TODO: attach event listeners
		#TODO: load blacklist (when site is set?)
		
		login=Gtk.Button(label="Login")
		buttonRow.pack_start(login, expand=False, fill=True, padding=0)
		
		self.add(buttonRow)
		
		self.tags=gtk
		self.add(self.tags)
