import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

import urllib.request

class tileView(Gtk.Box):
	"""settings and stuff"""
	def __init__(self, booruWidget):
		"""set everything up"""
		super(tileView, self).__init__(orientation=Gtk.Orientation.VERTICAL)
		
		self.parent=booruWidget
		#main grid
		self.colums=6
		
		self.grid=Gtk.Grid()
		self.grid.set_column_homogeneous(True)
		#self.grid.set_row_homogeneous(True)
		
		scroll=Gtk.ScrolledWindow()
		scroll.add(self.grid)
		
		self.pack_start(scroll, expand=True, fill=True, padding=0)
		
		#viewer controls
		#TODO: implement
		
		self.cache={}
		self.client=None
		
	def refresh(self):
		#clear the grid
		tiles=self.grid.get_children()
		for tile in tiles:
			self.grid.remove(tile)
		
		def click(w, e, post):
			#print(post)
			self.parent.openImage(post)
		
		#fetch new results
		results=self.client.post_list(tags=self.query, page=self.page)
		#from pprint import pprint
		#pprint(results)
		def loadLoop():
			print("running loadLoop")
			(x, y)=(0, 0)
			for post in results:
				id=int(post["id"])
				#cach the post thumbnail if we dont already have it
				if not id in self.cache:
					#set up the response
					response=urllib.request.urlopen(post["preview_url"])
					#set the cache as an empty image now, just enough to add it to the grid
					self.cache[id]=Gtk.Image()
					#download incrementally on the gobject's idle
					def loadurl(image, response):
						loader=gi.repository.GdkPixbuf.PixbufLoader()
						buf=bytes()
						while True:
							read=response.read(512)
							if read:
								buf+=read
								yield True
							else:
								break;
						loader.write(buf)
						loader.close()
						image.set_from_pixbuf(loader.get_pixbuf())
						image.show()
						yield False
					GObject.idle_add(next, loadurl(self.cache[id], response))
					
					print("cached image id ", id)
				
				#take image from the cache and put it in the grid
				if x==self.colums:
					x=0
					y+=1
				
				clicker=Gtk.EventBox()
				clicker.add(self.cache[id])
				clicker.connect("button_press_event", click, post)
				clicker.show()
				self.grid.attach(clicker, x, y, 1, 1)
				
				print("attached {} to ({},{})".format(id, x, y))
				x+=1
				yield True
			yield False
		GObject.idle_add(next, loadLoop())
	
	def updateSearch(self, client, query):
		"""reset everything and update"""
		self.page=1
		#new client, reset the cache
		if not self.client is client:
			self.client=client
			self.cache={}
		self.query=query
		self.refresh()
