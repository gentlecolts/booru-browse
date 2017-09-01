#!/usr/bin/python3
print("Loading resources")

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject, Gdk

from mainwin import booruView

#windows console is a pain about unicode
#import os
#if os.name=='nt':
#import sys
#import codecs
#sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#sys.stderr = codecs.getwriter('utf8')(sys.stderr)

print("Browser is starting")

win=Gtk.Window()
win.connect("delete-event", lambda wid, event:Gtk.main_quit())
win.resize(1280, 720)
win.set_title("Booru Browser")

print("window created, adding content")

booruview=booruView()

#key navigation
navblockers=[Gtk.SearchEntry]
def keyfn(w, e):
	keyname=Gdk.keyval_name(e.keyval)
	#print(e.keyval, keyname)
	
	if type(w.get_focus()) in navblockers:
		#print("cant navigate while entry is selected")
		return
	
	if keyname=="Right":
		booruview.next(1)
	elif keyname=="Left":
		booruview.next(-1)
booruview.floater.connect('key_press_event', keyfn)
#self.postPreview.connect('key_press_event', keyfn)
#self.post.connect('key_press_event', keyfn)
win.connect('key_press_event', keyfn)

def clickEvent(w, e):
	print(type(w))
	print(dir(e))
	win.set_focus(None)

booruview.connect("button-press-event", clickEvent)

win.add(booruview)
win.show()

print("content created, starting program")

GObject.threads_init()
Gtk.main()
