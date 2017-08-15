import gi
gi.require_version("Gtk", "3.0")
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, WebKit

from tagContainer import tagBox

from Vinebooru import Vinebooru

tagkeys=['artist', 'tags']
#tagkeys=['tags']

#golden ratio
golden = (1 + 5 ** 0.5) / 2
panelWid=int(1280*(1-1/golden)/2)

#TODO: clean this up
class tagDisplay(Gtk.ScrolledWindow):
#class tagDisplay(Gtk.Box):
	def __init__(self, container, tags:tagBox):
		super(tagDisplay, self).__init__()
		#super(tagDisplay, self).__init__(Gtk.Orientation.VERTICAL)
		self.tags=tags
		self.parent=container
		
		self.box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		#self.box.set_homogeneous(True)
		#self.box=Gtk.Grid()
		#self.box.set_column_homogeneous(True)
		#self.box.set_alignment(0, 0)
		
		port=Gtk.Viewport()
		port.add(self.box)
		self.add(port)
		#self.add(self.box)
		#self.show_all()
		self.set_size_request(100, 720)
	
	def setContent(self, content:dict):
		"""add stuff to the widget"""
		#clean anything currently here
		children=self.box.get_children()
		for child in children:
			self.box.remove(child)
		
		y=0
		def addgrid(widget):
			nonlocal y
			self.box.attach(widget, 0, y, 1, 1)
			y+=1
		
		from pprint import pprint
		pprint(content)
		width=0
		for category, tags in sorted(content.items()):
			catlab=Gtk.Label(category)
			catlab.set_alignment(0, 0)
			self.box.add(catlab)
			#addgrid(Gtk.Label(category))
			
			if type(tags) is str:
				tags=tags.split()
			for tag in tags:
				button=Gtk.LinkButton.new_with_label(tag, tag)
				def click(button):
					#print(dir(button))
					self.tags.addTags([button.get_uri()])
					return True#needed to override default click behavior
				button.connect('activate-link', click)
				#button.get_children()[0].set_justify(Gtk.Justification.LEFT)
				button.set_alignment(0, 0)
				#button=Gtk.Label(tag)
				self.box.pack_start(button, expand=False, fill=False, padding=0)
				
				#self.box.add(button)
				#addgrid(button)
				
				#print("added {}:{}".format(category, tag))
				width=max(width, button.get_allocation().width)
				
				#req=button.get_size_request()
				#print(req.width, req.height)
				#print(button.size_request())
		
		self.set_size_request(panelWid, self.parent.get_size_request().height)
		#self.show_all()

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
		contentBox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		
		self.sources=sourceDisplay()
		self.comments=commentDisplay()
		self.tags=tagDisplay(contentBox, booruWidget.search.tags)
		
		self.getClient=booruWidget.search.getClient
		
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
		
		def makeToggle(name, target):
			frame=Gtk.Frame(label=name)
			button=Gtk.Switch()
			frame.add(button)
			
			def onswitch(switch, param):
				if switch.get_active():
					target.show_all()
					
					"""
					def listchildren(widget, space=''):
						print(name, space, type(widget))
						try:
							children=widget.get_children()
						except:
							children=[]
						space=space+' '
						for child in children:
							listchildren(child, space)
					
					listchildren(target)
					"""
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
		client=self.getClient()
		#TODO: for future special cases, maybe this should depend on a key in the dict instead of class type
		if type(client) is Vinebooru:
			client.fetchPost(post)
		
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
