import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from tagContainer import tagBox
from listBoorus import booruLister
import blacklist
import BooruIcon

class searchWidget(Gtk.Box):
	"""search bar"""
	def __init__(self, booruWidget):
		"""set everything up"""
		super(searchWidget, self).__init__(orientation=Gtk.Orientation.VERTICAL)
		
		buttonRow=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		
		self.booruWidget=booruWidget
		
		#search related buttons
		self.searchbar=Gtk.SearchEntry()
		buttonRow.pack_start(self.searchbar, expand=True, fill=True, padding=0)
		
		searchbutton=Gtk.Button(label="Update Search")
		buttonRow.pack_start(searchbutton, expand=False, fill=True, padding=0)
		def updateSearch(button):
			newtags=self.searchbar.get_text().split()
			self.searchbar.set_text("")
			self.tags.addTags(newtags)
		searchbutton.connect("clicked", updateSearch)
		self.searchbar.connect("activate", updateSearch)
		
		resetbutton=Gtk.Button(label="Reset Search")
		buttonRow.pack_start(resetbutton, expand=False, fill=True, padding=0)
		def resetSearch(button):
			self.tags.clear()
		resetbutton.connect("clicked", resetSearch)
		
		#single window mode button
		self.single=Gtk.ToggleButton('Single Window Mode')
		def onToggle(widget):
			booruWidget.setSingleWin(widget.get_active())
		self.single.connect('toggled', onToggle)
		
		buttonRow.pack_start(self.single, expand=True, fill=False, padding=0)
		
		#settings related buttons
		self.boorus=booruLister(booruWidget)
		buttonRow.pack_start(self.boorus, expand=False, fill=True, padding=0)
		
		blocklister=Gtk.Button(label="Blocklist")
		buttonRow.pack_start(blocklister, expand=False, fill=True, padding=0)
		blocklister.connect("clicked", lambda b:blacklist.gui_edit())
		
		showBlacklist=Gtk.ToggleButton('Show Blacklisted')
		def blacklistSwitch(widget):
			BooruIcon.showBlocked=widget.get_active()
		showBlacklist.connect('toggled', blacklistSwitch)
		buttonRow.pack_start(showBlacklist, expand=False, fill=False, padding=0)
		
		login=Gtk.Button(label="Login")
		buttonRow.pack_start(login, expand=False, fill=True, padding=0)
		#TODO: attach event listeners
		#TODO: what login info can be stored securely (username? tokens?)?
		login.set_sensitive(False)#TODO: remove this when button works
		
		self.add(buttonRow)
		
		self.tags=tagBox(self)
		self.add(self.tags)
		
		#alias this for convenience
		self.tagsAsString=self.tags.tagsAsString
	
	def getClient(self):
		return self.boorus.booru
