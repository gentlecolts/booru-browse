import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import pybooru
from Vinebooru import Vinebooru

defText="""#any non-stock boorus go here, i make no guarentee if they'll work or not
#broken site reports would be appreciated, but are more likely an issue with pybooru than with this program

#line format: site	api_version
#api version is optional
#empty lines and lines beginning with # are ignored
#as of right now, custom sites can only be moebooru-based sites, support for plain danbooru ones should be coming sometime eventually

#some examples:

#sites can be full urls, or just the domain
#note that because some sites dont support https, http will be used by default if https is not provided
#site.com
#http://site.com
#https://site.com

#valid versions are shown here, shouldnt be needed unless a site doesnt work right
#site.com	1.13.0
#site.com	1.13.0+update.1
#site.com	1.13.0+update.2
"""

class booruLister(Gtk.ComboBoxText):
	def __init__(self, booruWidget):
		super(booruLister, self).__init__()
		
		self.sites=["danbooru","konachan","vinebooru"]
		self.booru=None
		self.parent=booruWidget
		
		try:
			with open("boorus.txt") as f:
				for line in f.readlines():
					line=line.strip()
					if line and not line.startswith("#"):
						self.sites.append(line.split())
		except FileNotFoundError:
			with open('boorus.txt', 'w') as f:
				f.write(defText)
		
		for booru in self.sites:
			if type(booru) is str:
				self.append_text(booru)
			else:#a list
				self.append_text(booru[0])
		
		self.connect("changed", self.setBooru)
	
	def setBooru(self, selection):
		target=selection.get_active_text().lower()
		print("setting booru: ", target)
		
		#TODO: username/password/tokens/etc
		
		if target=='danbooru':
			self.booru=pybooru.Danbooru('danbooru')
		elif target=='konachan':
			self.booru=pybooru.Moebooru('konachan')

		elif target=='vinebooru':
			self.booru=Vinebooru()
		else:
			if not target.startswith('http'):
				target="http://"+target
			self.booru=pybooru.Moebooru(site_url=target, api_version="1.13.0+update.2")
		
		self.parent.updateSearch()
