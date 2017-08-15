import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

import urllib.request
from concurrent.futures import ThreadPoolExecutor

def loadurl(gtkimage, url):
	request=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	
	response=urllib.request.urlopen(request)
	loader=gi.repository.GdkPixbuf.PixbufLoader()
	
	loader.write(response.read())
	loader.close()
	
	GObject.idle_add(lambda:gtkimage.set_from_pixbuf(loader.get_pixbuf()))

class tileView(Gtk.Box):
	"""settings and stuff"""
	def __init__(self, booruWidget):
		"""set everything up"""
		super(tileView, self).__init__(orientation=Gtk.Orientation.VERTICAL)
		
		self.parent=booruWidget
		self.cache={}
		self.client=None
		self.page=1
		
		#main grid
		self.colums=7
		
		self.grid=Gtk.Grid()
		self.grid.set_column_homogeneous(True)
		#self.grid.set_row_homogeneous(True)
		
		scroll=Gtk.ScrolledWindow()
		scroll.add(self.grid)
		
		self.pack_start(scroll, expand=True, fill=True, padding=0)
		
		#viewer controls
		backbtn=Gtk.Button()
		backbtn.set_image(Gtk.Image(stock="gtk-go-back"))
		forwardbtn=Gtk.Button()
		forwardbtn.set_image(Gtk.Image(stock='gtk-go-forward'))
		
		backbtn.connect('clicked', lambda b:self.setPage(self.page-1))
		forwardbtn.connect('clicked', lambda b:self.setPage(self.page+1))
		
		pageFrame=Gtk.Frame(label="Page")
		self.pageEntry=Gtk.Entry()
		self.pageEntry.set_text(str(self.page))
		pageFrame.add(self.pageEntry)
		pageFrame.set_shadow_type(Gtk.ShadowType.NONE)
		
		def inputFilter(entry):
			entry.set_text(''.join([i for i in entry.get_text() if i in '0123456789']))
		self.pageEntry.connect('changed', inputFilter)
		def submit(entry):
			self.setPage(int(entry.get_text()))
		self.pageEntry.connect('activate', submit)
		
		controlBox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		controlBox.pack_start(Gtk.Fixed(), expand=True, fill=True, padding=0)
		controlBox.pack_start(backbtn, expand=False, fill=True, padding=10)
		controlBox.pack_start(pageFrame, expand=False, fill=True, padding=10)
		controlBox.pack_start(forwardbtn, expand=False, fill=True, padding=10)
		controlBox.pack_start(Gtk.Fixed(), expand=True, fill=True, padding=0)
		
		self.pack_start(controlBox, expand=False, fill=True, padding=0)
		self.show_all()
		
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
		
		#TODO: remove blacklisted items from results
		
		#from pprint import pprint
		#pprint(results)
		
		print("running loadLoop")
		(x, y)=(0, 0)
		cachepool=ThreadPoolExecutor()
		for post in results:
			id=int(post["id"])
			#cach the post thumbnail if we dont already have it
			if not id in self.cache:
				#set up the response
				
				#set the cache as an empty image now, just enough to add it to the grid
				self.cache[id]=Gtk.EventBox()
				cacheimage=Gtk.Image()
				
				self.cache[id].add(cacheimage)
				self.cache[id].connect("button_press_event", click, post)
				
				#TODO: is it possible to set image size request?  size info is in the json
				
				#determine the url for the preview
				preview=post['preview_url' if "preview_url" in post else 'preview_file_url']
				if not preview.startswith('http'):
					preview=self.client.site_url+preview
					
				#print(preview)
				
				#queue image for loading into cache
				cachepool.submit(loadurl, cacheimage, preview)
				#loadurl(cacheimage, preview)
				
				self.cache[id].show_all()
			
			#take image from the cache and put it in the grid
			if x==self.colums:
				x=0
				y+=1
			self.grid.attach(self.cache[id], x, y, 1, 1)
			x+=1
	
	def updateSearch(self, client, query):
		"""reset everything and update"""
		self.page=1
		#new client, reset the cache
		if not self.client is client:
			self.client=client
			self.cache={}
		self.query=query
		self.refresh()
	
	def setPage(self, page):
		self.page=0 if page<0 else page
		#print("setting page to ", page)
		self.pageEntry.set_text(str(self.page))
		self.refresh()
