import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def alert(source, msg, header="Uh oh, something broke"):
	dialog = Gtk.MessageDialog(source.get_toplevel(), 0, Gtk.MessageType.ERROR,
		Gtk.ButtonsType.CANCEL, header)
	dialog.format_secondary_text(msg)
	dialog.run()
	#print("ERROR dialog closed")
	dialog.destroy()
