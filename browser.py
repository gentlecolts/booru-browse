#!/usr/bin/python3
import gi
from pprint import pprint
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import pybooru

from mainwin import booruView

#client=pybooru.Moebooru(site_url='https://booru.vineshroom.net', api_version="1.13.0+update.2")
client=pybooru.Moebooru(site_url='https://e926.net', api_version="1.13.0+update.2")

#print(len(client.post_list(tags="zangoose", page=2)))
#pprint(client.post_list(tags="zangoose"))

win=Gtk.Window()
win.connect("delete-event", lambda wid, event:Gtk.main_quit())
win.set_size_request(1280, 720)

booruview=booruView(client)
win.add(booruview)
win.show_all()

Gtk.main()
