#!/usr/bin/python3
print("Loading resources")

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

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
win.add(booruview)
win.show()

print("content created, starting program")

GObject.threads_init()
Gtk.main()
