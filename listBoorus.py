import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import pybooru

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
		booru=None
		
		self.connect("changed", self.setBooru)
	
	def setBooru(self, selection):
		print(selection.get_active_text())
