import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

active_color=Gdk.RGBA(105.0/255,229.0/255,92.0/255, 1)
negate_color=Gdk.RGBA(229.0/255,92.0/255,105.0/255, 1)

class taglabel(Gtk.Box):
	def __init__(self, owner, tag):
		super(taglabel, self).__init__(orientation=Gtk.Orientation.HORIZONTAL)
		
		self.negated='-' if tag.startswith('-') else ''
		
		#name is tagname without negation if present
		self.name=tag[1:] if self.negated else tag
		
		self.label=Gtk.Label(tag)
		self.pack_start(self.label, expand=True, fill=True, padding=0)
		
		#create the buttons
		self.flipbttn=Gtk.Image(stock=("gtk-add" if self.negated else "gtk-remove"))
		negEvent=Gtk.EventBox()
		def flipper(w, e):
			self.flip()
			owner.refreshList()
		negEvent.add(self.flipbttn)
		negEvent.connect("button_press_event", flipper)
		self.pack_start(negEvent, expand=False, fill=True,padding=0)
		
		closeEvent=Gtk.EventBox()
		closeEvent.add(Gtk.Image(stock="gtk-close"))
		def closeme(w, e):
			owner.removeTag(self.name)
		closeEvent.connect("button_press_event", closeme)
		self.pack_start(closeEvent, expand=False, fill=True,padding=0)
		
		self.override_background_color(Gtk.StateType.NORMAL, negate_color if self.negated else active_color)

	def flip(self):
		self.negated='' if self.negated else '-'
		self.label.set_text(self.negated+self.name)
		#ICON_SIZE_SMALL_TOOLBAR
		
		self.flipbttn.set_from_icon_name(
			"gtk-add" if self.negated else "gtk-remove",
			Gtk.IconSize.SMALL_TOOLBAR
		)
		self.override_background_color(Gtk.StateType.NORMAL, negate_color if self.negated else active_color)

tagsPerRow=10

class tagBox(Gtk.Grid):
	def __init__(self, owner):
		super(tagBox, self).__init__()
		
		self.taglist={}
		
		self.set_margin_left(5)
		self.set_margin_right(5)
		self.set_column_spacing(10)
		
		self.parent=owner
		
	def refreshList(self):
		print("refreshing list")
		currentTags=self.get_children()
		for tag in currentTags:
			self.remove(tag)
		
		(x, y)=(0, 0)
		for key, val in sorted(self.taglist.items()):
			if x>=tagsPerRow:
				x=0
				y+=1
			self.attach(val, x, y, 1, 1)
			x+=1
		self.show_all()
		
		#need to display everything
		self.parent.booruWidget.updateSearch()
			
	def addTags(self, tags):
		for tag in tags:
			newtag=taglabel(self, tag)
			self.taglist[newtag.name]=newtag
		self.refreshList()
	
	def removeTag(self, tag):
		tag=self.taglist.pop(tag, None)
		if tag:
			print("removed {}".format(tag.name))
		self.refreshList()

	def clear(self):
		self.taglist={}
		self.refreshList()
	
	def tagsAsString(self):
		tags=[]
		for key, val in self.taglist.items():
			tags.append(val.negated+val.name)
		return ' '.join(tags)
