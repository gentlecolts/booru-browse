import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import pybooru
from Vinebooru import Vinebooru

class booruLister(Gtk.ComboBoxText):
	def __init__(self):
		super(booruLister, self).__init__()
		
		self.sites=["danbooru","konchan","vinebooru"]
		
		try:
			with open("boorus.txt") as f:
				for line in f.readlines():
					if line and not line.startswith("#"):
						self.sites.append(line.split())
		except FileNotFoundError:
			print("Couldnt find boorus.txt, skipping")
		
		for booru in self.sites:
			if type(booru) is str:
				self.append_text(booru)
			else:#a list
				self.append_text(booru[0])
		self.booru=None
		
		self.connect("changed", self.setBooru)
	
	def setBooru(self, selection):
		target=selection.get_active_text().lower()
		if not target.startswith('http'):
			target="https://"+target
		print("setting booru: ", target)
		
		#TODO: username/password/tokens/etc
		
		if target=='danbooru':
			self.booru=pybooru.Danbooru('danbooru')
		elif target=='konachan':
			self.booru=pybooru.Moebooru('konachan')
		elif target=='vinebooru':
			self.booru=Vinebooru()
		else:
			self.booru=pybooru.Moebooru(target)
