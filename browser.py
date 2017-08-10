#!/usr/bin/python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

from mainwin import booruView

win=Gtk.Window()
win.connect("delete-event", lambda wid, event:Gtk.main_quit())
win.set_size_request(1280, 720)

booruview=booruView()
win.add(booruview)
win.show_all()

GObject.threads_init()
Gtk.main()
