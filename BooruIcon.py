import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GdkPixbuf

import urllib.request
from concurrent.futures import ThreadPoolExecutor
import blacklist

try:
	#python > 3.4 makes max workers equal to number of cores by default
	cachepool=ThreadPoolExecutor()
except:
	#but if this needs a parameter, just give it one
	cachepool=ThreadPoolExecutor(max_workers=8)

blockPbuf=GdkPixbuf.Pixbuf.new_from_file("blocked.png")
activePost=None

#TODO: ui button for this
showBlocked=False

(EMPTY, LOADED, HIDDEN)=range(3)

class BooruIcon(Gtk.EventBox):
	def __init__(self, url, post, onClick, *args):
		super(BooruIcon, self).__init__()
		
		self.display=Gtk.Image()
		#self.post=post
		self.id=post['id']
		self.blocked=blacklist.is_blocked(post['tags'])
		self.pixbuf=None
		self.state=EMPTY
		
		def loadurl():
			request=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
			
			response=urllib.request.urlopen(request)
			loader=GdkPixbuf.PixbufLoader()
			
			loader.write(response.read())
			loader.close()
			
			self.pixbuf=loader.get_pixbuf()
			#print("done loading")
			
			#GObject.idle_add(lambda:self.display.set_from_pixbuf(self.pixbuf))
		
		#queue image for loading into cache
		cachepool.submit(loadurl)
		
		#TODO: if blacklisted, add blacklist image instead
		self.add(self.display)
		self.connect("button_press_event", onClick, *args)
		
		self.show_all()
		
		def hide_preview():
			self.display.set_from_pixbuf(blockPbuf)
			self.state=HIDDEN
		def show_preview():
			self.display.set_from_pixbuf(self.pixbuf)
			self.state=LOADED
		
		def idleLoop():
			if self.state==EMPTY:
				if self.blocked:
					hide_preview()
				elif self.pixbuf:
					show_preview()
			elif self.state==HIDDEN and showBlocked and self.pixbuf:
				show_preview()
			elif self.state==LOADED and self.blocked and not showBlocked:
				hide_preview()
			#show border if active post
			#if activePost==self.id:
			#else
			return True
		
		GObject.idle_add(idleLoop)
