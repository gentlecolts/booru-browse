import gi
gi.require_version("Gtk", "3.0")
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, WebKit

#tagkeys=['artist', 'tags']
tagkeys=['tags']

class tagDisplay(Gtk.ScrolledWindow):
	def __init__(self, tags):
		super(tagDisplay, self).__init__()
		self.tags=tags
		self.box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		port=Gtk.Viewport()
		port.add(self.box)
		self.add(port)
	
	def setContent(self, content):
		"""add stuff to the widget"""
		#clean anything currently here
		children=self.box.get_children()
		for child in children:
			self.box.remove(child)
		
		from pprint import pprint
		pprint(content)
		for category, tags in content.items():
			self.box.add(Gtk.Label(category))
			if type(tags) is str:
				tags=tags.split()
			for tag in tags:
				button=Gtk.LinkButton.new_with_label(tag, tag)
				def click(button):
					self.tags.addTags([button.uri])
					return True#needed to override default click behavior
				button.connect('activate-link', click)
				
				self.box.pack_start(button, expand=False, fill=True, padding=0)
				
				#print("added {}:{}".format(category, tag))
		self.show_all()

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
	
	def setContent(self, content):
		"""add stuff to the widget"""

class postView(Gtk.Box):
	"""settings and stuff"""
	def __init__(self, booruWidget):
		"""set everything up"""
		super(postView, self).__init__(orientation=Gtk.Orientation.VERTICAL)
		
		#comments, tags, and sources
		self.sources=sourceDisplay()
		self.comments=commentDisplay()
		self.tags=tagDisplay(booruWidget.search.tags)
		
		#web view for displaying media
		self.content=WebKit.WebView()
		
		#pull content together
		sw=Gtk.ScrolledWindow()
		sw.add(self.content)
		sw.show_all()
		
		midbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		midbox.pack_start(sw, expand=True, fill=True, padding=0)
		midbox.pack_start(self.sources, expand=False, fill=True, padding=0)
		midbox.show()
		
		contentBox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		contentBox.pack_start(self.tags, expand=False, fill=True, padding=0)
		contentBox.pack_start(midbox, expand=True, fill=True, padding=0)
		contentBox.pack_start(self.comments, expand=False, fill=True, padding=0)
		contentBox.show()
		
		#pack everything into a neat box
		self.pack_start(contentBox, expand=True, fill=True, padding=0)
		
		#set up bottom utility bar
		backbtn=Gtk.Button(stock='gtk-go-back')
		backbtn.set_image(Gtk.Image(stock="gtk-go-back"))
		backbtn.connect("clicked", lambda btn:booruWidget.closeImage())
		
		#TODO: make this accept a "target", switch should hide/show the target
		def makeToggle(name, target):
			frame=Gtk.Frame(label=name)
			button=Gtk.Switch()
			frame.add(button)
			
			def onswitch(switch, param):
				if switch.get_active():
					target.show_all()
				else:
					target.hide()
			
			button.connect("notify::active",onswitch)
			
			return (frame, button)
		
		(tagframe, self.tagSwitch)=makeToggle("Tags", self.tags)
		(commentframe, self.commentSwitch)=makeToggle("Comments", self.comments)
		(sourceframe, self.sourceSwitch)=makeToggle("Source", self.sources)
		
		bottomBar=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		bottomBar.pack_start(backbtn, expand=False, fill=True, padding=0)
		bottomBar.pack_start(Gtk.Fixed(), expand=True, fill=True, padding=0)
		bottomBar.pack_start(tagframe, expand=False, fill=True, padding=0)
		bottomBar.pack_start(commentframe, expand=False, fill=True, padding=0)
		bottomBar.pack_start(sourceframe, expand=False, fill=True, padding=0)
		bottomBar.show_all()
		
		self.pack_start(bottomBar, expand=False, fill=True, padding=0)
	
	def load(self, post):
		url=post['file_url']
		self.content.load_uri(url)
		
		tags={}
		for key in tagkeys:
			if key in post:
				tags[key]=post[key]
		self.tags.setContent(tags)
		
		sources=[post['source']]
		if 'sources' in post:
			sources+=post['sources']
		self.sources.setContent(sources)
		
		#self.comments.setContent()
