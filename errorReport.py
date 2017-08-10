import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def alert(source, msg):
	dialog = Gtk.MessageDialog(source.get_toplevel(), 0, Gtk.MessageType.ERROR,
		Gtk.ButtonsType.CANCEL, "Uh oh, something broke")
	dialog.format_secondary_text(msg)
	dialog.run()
	#print("ERROR dialog closed")
	dialog.destroy()
