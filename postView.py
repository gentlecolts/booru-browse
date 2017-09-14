import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from tagContainer import tagBox
from Vinebooru import Vinebooru
from DynamicMedia import DynamicMedia

tagkeys=['artist', 'tags']

#golden ratio
golden = (1 + 5 ** 0.5) / 2
panelWid=int(1280*(1-1/golden)/2)

class tagDisplay(Gtk.ScrolledWindow):
	def __init__(self, container, tags:tagBox):
		super(tagDisplay, self).__init__()
		self.tags=tags
		self.parent=container
		
		self.box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		port=Gtk.Viewport()
		port.add(self.box)
		self.add(port)
	
	def setContent(self, content:dict):
		"""add stuff to the widget"""
		#clean anything currently added
		children=self.box.get_children()
		for child in children:
			self.box.remove(child)
			#TODO: child.destroy()
		
		y=0
		def addgrid(widget):
			nonlocal y
			self.box.attach(widget, 0, y, 1, 1)
			y+=1
		
		#from pprint import pprint
		#pprint(content)
		width=0
		for category, tags in sorted(content.items()):
			catlab=Gtk.Label(category)
			catlab.set_alignment(0, 0)
			self.box.add(catlab)
			
			if type(tags) is str:
				tags=tags.split()
			for tag in tags:
				button=Gtk.LinkButton.new_with_label(tag, tag)
				def click(button):
					self.tags.addTags([button.get_uri()])
					return True#needed to override default click behavior
				button.connect('activate-link', click)
				button.set_alignment(0, 0)
				self.box.pack_start(button, expand=False, fill=False, padding=0)
				
				width=max(width, button.get_allocation().width)
		
		self.set_size_request(panelWid, self.parent.get_size_request().height)

class sourceDisplay(Gtk.Box):
	def __init__(self):
		super(sourceDisplay, self).__init__(orientation=Gtk.Orientation.VERTICAL)
	
	def setContent(self, content):
		"""add as many Gtk.LinkButton to the widget as needed"""
		#clean anything currently here
		children=self.get_children()
		for child in children:
			self.remove(child)
		
		#add new content
		for source in content:
			button=Gtk.LinkButton.new_with_label(source, source)
			self.pack_start(button, expand=False, fill=True, padding=0)


class commentDisplay(Gtk.ScrolledWindow):
	def __init__(self):
		super(commentDisplay, self).__init__()
		self.comments=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.comments)
	
	def setContent(self, content):
		children=self.comments.get_children()
		for child in children:
			self.comments.remove(child)
		
		for comment in content:
			print("adding comment", comment)
			c=Gtk.Frame(label=comment['username'])
			box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
			#TODO: pretty format the time
			box.add(Gtk.Label(comment['time']))
			
			combox=Gtk.TextView()
			combox.get_buffer().set_text(comment['text'])
			combox.set_editable(False)
			combox.set_cursor_visible(False)
			combox.set_wrap_mode(Gtk.WrapMode.WORD)
			box.add(combox)
			c.add(box)
			self.comments.add(c)
		self.comments.show_all()
		self.set_size_request(panelWid, -1)

class postView(Gtk.Box):
	"""settings and stuff"""
	def __init__(self, booruWidget):
		"""set everything up"""
		super(postView, self).__init__(orientation=Gtk.Orientation.VERTICAL)
		
		#comments, tags, and sources
		contentBox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		
		self.sources=sourceDisplay()
		self.comments=commentDisplay()
		self.tags=tagDisplay(contentBox, booruWidget.search.tags)
		
		self.getClient=booruWidget.search.getClient
		
		#web view for displaying media
		self.content=DynamicMedia()
		
		#pull content together
		sw=Gtk.ScrolledWindow()
		sw.add(self.content)
		sw.show_all()
		
		self.midbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.midbox.pack_start(sw, expand=True, fill=True, padding=0)
		self.midbox.pack_end(self.sources, expand=False, fill=True, padding=0)
		self.midbox.show()
		
		contentBox.pack_start(self.tags, expand=False, fill=True, padding=0)
		contentBox.pack_start(self.midbox, expand=True, fill=True, padding=0)
		contentBox.pack_start(self.comments, expand=False, fill=True, padding=0)
		contentBox.show()
		
		self.media=contentBox
		
		#set up utility bar
		self.backbtn=Gtk.Button(stock='gtk-go-back')
		self.backbtn.set_always_show_image(True)
		self.backbtn.connect("clicked", lambda btn:booruWidget.closeImage())
		
		savebtn=Gtk.Button("Save Image")
		savebtn.connect('clicked', lambda b:self.content.saveDialog(self.get_toplevel()))
		
		prev=Gtk.Button(stock='gtk-media-previous')
		prev.set_always_show_image(True)
		
		next=Gtk.Button(stock='gtk-media-next')
		next.set_always_show_image(True)
		next.set_image_position(Gtk.PositionType.RIGHT)
		
		#even though this maybe seems not specially intuitive, having next go to newer posts seems to be the best approach
		prev.connect("clicked", lambda b:booruWidget.next(1))
		next.connect("clicked", lambda b:booruWidget.next(-1))
		
		#TODO: clean up this function
		def makeToggle(name, target):
			button=Gtk.ToggleButton(name)
			
			def onswitch(switch):
				if switch.get_active():
					target.show_all()
				else:
					target.hide()
			
			button.connect("toggled",onswitch)
			
			return button
		
		self.tagSwitch=makeToggle("Tags", self.tags)
		self.commentSwitch=makeToggle("Comments", self.comments)
		self.sourceSwitch=makeToggle("Source", self.sources)
		
		navbuttons=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		navbuttons.pack_start(prev, expand=False, fill=True, padding=5)
		navbuttons.pack_start(next, expand=False, fill=True, padding=5)
		
		#TODO:toggle button for upscaling
		togglebuttons=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		togglebuttons.pack_start(Gtk.Label("Viewer Switches: "), expand=False, fill=True, padding=0)
		togglebuttons.pack_start(self.tagSwitch, expand=False, fill=True, padding=5)
		togglebuttons.pack_start(self.commentSwitch, expand=False, fill=True, padding=5)
		togglebuttons.pack_start(self.sourceSwitch, expand=False, fill=True, padding=5)
		
		self.upscale=Gtk.ToggleButton("Upscaling")
		def toggleUpscale(switch):
			self.content.allowUpscale=switch.get_active()
		self.upscale.connect("toggled",toggleUpscale)
		self.upscale.set_active(True)
		
		togglebuttons.pack_start(self.upscale, expand=False, fill=True, padding=5)
		
		#assemble the toolbar
		self.toolbar=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.toolbar.pack_start(self.backbtn, expand=True, fill=False, padding=0)
		self.toolbar.pack_start(savebtn, expand=True, fill=False, padding=0)
		self.toolbar.pack_start(navbuttons, expand=True, fill=False, padding=5)
		self.toolbar.pack_start(togglebuttons, expand=True, fill=False, padding=0)
		self.toolbar.show_all()
		
		
		#put it all together
		self.pack_start(self.toolbar, expand=False, fill=True, padding=0)
		self.pack_end(contentBox, expand=True, fill=True, padding=0)
	
	def load(self, post):
		client=self.getClient()
		#TODO: for future special cases, maybe this should depend on a key in the dict instead of class type
		if type(client) is Vinebooru:
			client.fetchPost(post)
		
		url=post['file_url']
		self.content.load(url=url)
		
		tags={}
		for key in tagkeys:
			if key in post:
				tags[key]=post[key]
		self.tags.setContent(tags)
		if(self.tagSwitch.get_active()):
			self.tags.show_all()
		
		sources=[post['source']]
		if 'sources' in post:
			sources+=post['sources']
		self.sources.setContent(sources)
		if(self.sourceSwitch.get_active()):
			self.sources.show_all()
		
		if 'comments' in post:
			self.comments.setContent(post['comments'])
	
	def removeMedia(self):
		self.remove(self.media)
		self.remove(self.toolbar)
		#self.backbtn.hide()
		self.backbtn.set_sensitive(False)
	
	def addMedia(self):
		self.pack_end(self.media, expand=True, fill=True, padding=0)
		self.pack_start(self.toolbar, expand=False, fill=True, padding=0)
		#self.backbtn.show()
		self.backbtn.set_sensitive(True)
