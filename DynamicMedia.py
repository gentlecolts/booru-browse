#!/usr/bin/python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GdkPixbuf

import urllib.request
import os
from threading import Thread

try:
	import math
	inf=math.inf
except:
	inf=float("inf")

scale_method=GdkPixbuf.InterpType.BILINEAR

class DynamicMedia(Gtk.EventBox):
	def __init__(self, path=None, url=None):
		super(DynamicMedia, self).__init__()
		
		self.media=Gtk.Image()
		
		self.name=""
		self.buf=None
		self.fit=True
		self.allowUpscale=True
		
		def toggle(w, e):
			self.fit=not self.fit
		
		self.connect("button_press_event", toggle)
		
		#TODO: Drag n drop support
		#self.connect('expose-event', self.on_image_resize)
		
		overlay=Gtk.Overlay()
		overlay.add(self.media)
		
		self.progressbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		overlay.add_overlay(self.progressbox)
		
		self.add(overlay)
		
		GObject.idle_add(self.resizeSelf)
		self.load(path, url)
	
	def load(self, path=None, url=None):
		if path:
			self.name=os.path.basename(path)
			self.buf=GdkPixbuf.PixbufAnimation.new_from_file(path)
			self.iter=self.buf.get_iter()
			self.media.set_from_animation(self.buf)
		elif url:
			#TODO:if url is cached, load it from cache and return before any of this
			loadbar=Gtk.ProgressBar()
			loadbar.set_text(url)
			loadbar.show()
			self.progressbox.add(loadbar)
			def asyncload():
				request=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
				source=urllib.request.urlopen(request)
				
				loader=GdkPixbuf.PixbufLoader()
				
				loader.write(source.read())
				loader.close()
				
				self.name=source.info().get_filename()
				print("got filename: ", self.name)
				
				self.buf=loader.get_animation()
				self.iter=self.buf.get_iter()
				
				def finish():
					self.media.set_from_animation(self.buf)
					self.progressbox.remove(loadbar)
					return False
				
				GObject.idle_add(finish)
			
			t=Thread(target=asyncload, daemon=True)
			t.start()
		else:
			#TODO: in the future, should empty current content
			return

	def resizeSelf(self):
		if not self.buf:
			return True
		
		container=self.get_parent().get_allocation()
			
		(x, y)=(container.width, container.height)
		(realx, realy)=(self.buf.get_width(), self.buf.get_height())
		
		scale=min(x/realx, y/realy, inf if self.allowUpscale else 1) if self.fit else 1
		
		(x, y)=(scale*realx, scale*realy)
		
		if self.buf.is_static_image():
			self.media.set_from_pixbuf(
				self.buf.get_static_image().scale_simple(x,y,scale_method)
			)
		elif hasattr(self, 'iter') and self.iter.advance():
			self.media.set_from_pixbuf(
				self.iter.get_pixbuf().scale_simple(x,y,scale_method)
			)
			#TODO: the best approach here might just be doing the animation stepping myself, for both static and not
			#self.media.set_from_animation(pixbuf_anim_copy_resize(self.buf, x, y))
		return True

if __name__=="__main__":
	win=Gtk.Window()
	win.connect("delete-event", lambda wid, event:Gtk.main_quit())
	win.set_size_request(320, 240)
	win.set_title("Title")
	
	#img=DynamicMedia('8db.jpg')
	img=DynamicMedia('54a.gif')
	#img=DynamicMedia('Red-Big-Frog-Wallpaper-Photos-202.jpg')
	#img=DynamicMedia(url='http://i0.kym-cdn.com/photos/images/newsfeed/001/256/886/074.gif')
	sw=Gtk.ScrolledWindow()
	sw.add(img)
	win.add(sw)
	win.show_all()

	GObject.threads_init()
	Gtk.main()

