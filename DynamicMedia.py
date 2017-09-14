#!/usr/bin/python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, GdkPixbuf, Gdk

import tempfile
import cgi,posixpath
import time

import urllib.request,urllib.parse
import os
from shutil import copyfile
from threading import Thread

try:
	import math
	inf=math.inf
except:
	inf=float("inf")

scale_method=GdkPixbuf.InterpType.BILINEAR

(TARGET_ENTRY_TEXT, TARGET_ENTRY_PIXBUF) = range(2)
(COLUMN_TEXT, COLUMN_PIXBUF) = range(2)

DRAG_ACTION = Gdk.DragAction.COPY

tempdirobj=tempfile.TemporaryDirectory(prefix="booru-browse-")
tempdir=tempdirobj.name+"/"
print("using tempdir:",tempdir)

def getName(url,content):
	domain=urllib.parse.urlsplit(url).netloc
	
	disposition=content.getheader('content-disposition')
	if disposition:
		_,params=cgi.parse_header(disposition)
		return domain,params['filename']
	else:
		return domain,posixpath.basename(urllib.parse.urlsplit(url).path)

imgcache={}

def loadWithProgress(url, progress):
	request=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	content=urllib.request.urlopen(request)
	buff=bytes()
	
	length=content.getheader('content-length')
	domain,name=getName(url,content)
	
	#print(domain,name)
	if length:
		length=int(length)
		blocksize=max(4096, length//100)
	else:
		"set up pulsing progress bar"
	
	def progUpdate():
		have=len(buff)
		if have<length:
			progress.set_fraction(have/length)
			return True
		return False
	GObject.idle_add(progUpdate)
	
	timer=time.time()
	while True:
		read=content.read(blocksize)
		if read:
			buff+=read
		else:
			break
	timer=time.time()-timer
	
	print("{}\n\ttook {:.2f} seconds, speed was {:.2f} KB/s".format(url, timer, len(buff)/(timer*1024)))
	
	#cache the image
	path=tempdir+domain
	if not os.path.exists(path):
		os.mkdir(path)
	path="{}/{}".format(path,name)
	
	return path, name,buff

class DynamicMedia(Gtk.EventBox):
	def __init__(self, path=None, url=None):
		super(DynamicMedia, self).__init__()
		
		#some properties
		self.media=Gtk.Image()
		self.name=""
		self.buf=None
		self.path=None
		self.fit=True
		self.allowUpscale=True
		self.draggable=False
		self.lastPath=os.path.expanduser('~/Downloads')
		
		def toggle(w, e):
			self.fit=not self.fit
		
		self.connect("button_release_event", toggle)
		
		#actually send the data
		def data_get(widget,context,selection,info,evttime):
			print("drag dropped")
			
			#print(type(selection))
			#print(widget,context,selection,info,evttime)
			
			selection.set_uris(["file://"+self.path])
		self.connect('drag_data_get',data_get)
		
		#assemble everything
		overlay=Gtk.Overlay()
		overlay.add(self.media)
		
		self.progressbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		overlay.add_overlay(self.progressbox)
		
		self.add(overlay)
		
		GObject.idle_add(self.resizeSelf)
		self.load(path, url)
	
	def enableDrag(self):
		if os.name=='nt':
			print("Drag n Drop not supported on windows")
			return
		targets=[
			#Gtk.TargetEntry.new('image/x-xpixmap',0,TARGET_ENTRY_PIXBUF),
			Gtk.TargetEntry.new('text/uri-list',0,TARGET_ENTRY_PIXBUF),
			#Gtk.TargetEntry.new('text/plain',0,TARGET_ENTRY_TEXT),
		]
		self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK,targets,DRAG_ACTION)
		self.draggable=True
	
	def disableDrag(self):
		self.drag_source_unset()
		self.draggable=False
	
	def generateDrag(self):
		if self.draggable and self.buf:
			pbuf=self.buf.get_static_image()
			(x,y)=(pbuf.get_width(),pbuf.get_height())
		
			scale=128/max(x,y)
		
			self.drag_source_set_icon_pixbuf(pbuf.scale_simple(scale*x,scale*y,scale_method))
	
	def load(self, path=None, url=None):
		if path:
			self.name=os.path.basename(path)
			with open(path,'rb') as f:
				#TODO: make copy in temp dir?
				self.path=path
				loader=GdkPixbuf.PixbufLoader()
				loader.write(f.read())
				loader.close()
				
				#self.buf=GdkPixbuf.PixbufAnimation.new_from_file(path)
				self.buf=loader.get_animation()
				self.iter=self.buf.get_iter()
				self.media.set_from_animation(self.buf)
				self.enableDrag()
				
				self.generateDrag()
			
		elif url:
			#if cached, use cached image
			if url in imgcache:
				self.load(path=imgcache[url])
				return
			
			loadbar=Gtk.ProgressBar()
			#if this is unset, then the displayed text will be the load percent
			#that said,
			#loadbar.set_text(url)
			
			loadbar.show()
			self.progressbox.add(loadbar)
			def asyncload():
				
				loader=GdkPixbuf.PixbufLoader()
				
				#these need to be stored separate from the self versions to prevent race conditions in cache
				path, name,buff=loadWithProgress(url, loadbar)
				(self.path,self.name)=(path, name)
				loader.write(buff)
				loader.close()
				
				#self.name=source.info().get_filename()
				#print("got filename: ", self.name)
				
				self.buf=loader.get_animation()
				self.iter=self.buf.get_iter()
				
				def finish():
					self.media.set_from_animation(self.buf)
					self.progressbox.remove(loadbar)
					self.enableDrag()
					self.generateDrag()
					return False
				
				GObject.idle_add(finish)
				
				#flush to disk in background
				with open(path,'wb+') as f:
					f.write(buff)
					imgcache[url]=path
			
			t=Thread(target=asyncload, daemon=True)
			t.start()
		else:
			#TODO: in the future, should empty current content
			self.disableDrag()
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
	
	def saveDialog(self, rootwin=None):
		#TODO: wait (in bg thread) to ensure disk file is fully written before opening save dialog
		if not self.path:
			print("no image loaded, cant save")
			return
		
		print("saving media!")
		dialog=Gtk.FileChooserDialog(
			"Save image", rootwin,
			Gtk.FileChooserAction.SAVE, 
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
		)
		
		print("default name should be:", self.name)
		dialog.set_current_folder(self.lastPath)
		dialog.set_current_name(self.name)
		dialog.set_do_overwrite_confirmation(True)
		
		response=dialog.run()
		if response==Gtk.ResponseType.OK:
			saveto=dialog.get_filename()
			self.lastPath=os.path.dirname(saveto)
			print("saving to:", saveto)
			copyfile(self.path, saveto)
		elif response==Gtk.ResponseType.CANCEL:
			print("save canceled")
		dialog.destroy()

if __name__=="__main__":
	win=Gtk.Window()
	win.connect("delete-event", lambda wid, event:Gtk.main_quit())
	win.set_size_request(320, 240)
	win.set_title("Title")
	
	#img=DynamicMedia('8db.jpg')
	#img=DynamicMedia('54a.gif')
	#img=DynamicMedia('Red-Big-Frog-Wallpaper-Photos-202.jpg')
	img=DynamicMedia(url='http://i0.kym-cdn.com/photos/images/newsfeed/001/256/886/074.gif')
	sw=Gtk.ScrolledWindow()
	sw.add(img)
	win.add(sw)
	win.show_all()

	GObject.threads_init()
	Gtk.main()

