import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GdkPixbuf

import urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
import sqlite3

import blacklist

#sqlite stuff
conn=sqlite3.connect('viewedposts.db')
sql=conn.cursor()

def isPostViewed(domain, pid):
	sql.execute('SELECT * FROM sqlite_master WHERE name=?',[domain])
	if sql.fetchone():
		sql.execute("SELECT id FROM '{}' where id=?".format(domain), [pid])
		return sql.fetchone()
	return False

def sqlViewPost(domain, pid):
	#make a table for this domain if it doesnt exist, say id is unique
	sql.execute("CREATE TABLE IF NOT EXISTS '{}' (id int,UNIQUE(id))".format(domain))
	#insert the new value, dont complain about non-unique
	sql.execute("INSERT OR IGNORE INTO '{}' VALUES (?)".format(domain), [pid])
	conn.commit()

#set up the thread pool for icon loading
try:
	#python > 3.4 makes max workers equal to number of cores by default
	cachepool=ThreadPoolExecutor()
except:
	#but if this needs a parameter, just give it one
	cachepool=ThreadPoolExecutor(max_workers=8)

#blocked 
blockPbuf=GdkPixbuf.Pixbuf.new_from_file("blocked.png")

#TODO: ui button for this
showBlocked=False

(EMPTY, LOADED, HIDDEN)=range(3)

coverColor=0xffffff7f#rgba
coverfill=GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, 1, 1)
coverfill.fill(coverColor)
eyepbuf=GdkPixbuf.Pixbuf.new_from_file("eye.png")

class BooruIcon(Gtk.EventBox):
	def __init__(self, url, post, *args):
		super(BooruIcon, self).__init__()
		
		self.display=Gtk.Image()
		self.post=post
		self.id=post['id']
		self.blocked=blacklist.is_blocked(post['tags'])
		self.pixbuf=None
		self.state=EMPTY
		self.overlay=Gtk.Overlay()
		self.cover=Gtk.Image()#TODO: set from pixbuf, consider generating at runtime
		self.viewedicon=Gtk.Image()#TODO: set from pixbuf, consider generating at runtime
		self.domain=urllib.parse.urlsplit(post['preview_url']).netloc
		
		def loadurl():
			request=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
			
			response=urllib.request.urlopen(request)
			loader=GdkPixbuf.PixbufLoader()
			
			loader.write(response.read())
			loader.close()
			
			self.pixbuf=loader.get_pixbuf()
			
			def quickcheck():
				if isPostViewed(self.domain, int(self.id)):
					self.setViewed()
				return False
			GObject.idle_add(quickcheck)
			
			#print("done loading")
		
		#queue image for loading into cache
		cachepool.submit(loadurl)
		
		self.overlay.add(self.display)
		self.overlay.add_overlay(self.cover)
		self.overlay.add_overlay(self.viewedicon)
		
		self.add(self.overlay)
		self.show_all()
		#self.cover.hide()
		
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
			
			return True
		
		GObject.idle_add(idleLoop)
	
	def setViewed(self):
		#print("i am viewed now")
		self.cover.set_from_pixbuf(coverfill.scale_simple(self.pixbuf.get_width(), self.pixbuf.get_height(), GdkPixbuf.InterpType.BILINEAR))
		
		self.viewedicon.set_from_pixbuf(eyepbuf)
		self.viewedicon.props.halign=2
		self.viewedicon.props.valign=2
		
		sqlViewPost(self.domain,int(self.id))
