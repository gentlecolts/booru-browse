import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import pybooru
from Vinebooru import Vinebooru

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
			print("Couldnt find boorus.txt, skipping")
		
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
