import gi
gi.require_version("Gtk", "3.0")
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, GObject, WebKit

class queuedBar(Gtk.ProgressBar):
	def __init__(self):
		super(queuedBar, self).__init__()
		self.tasks=[]
		self.set_show_text("Caching Thumbnails")
		
		self.show()
		def watcher():
			#print("watching...")
			if len(self.tasks):
				#print("have tasks, updating")
				self.show()
				lis=self.tasks[0]
				if lis[0]<lis[1]:
					#print("progress: {}/{}".format(lis[0], lis[1]))
					self.set_fraction(lis[0]/lis[1])
				else:
					#print("top task finished")
					self.tasks.pop(0)
			else:
				#print("no tasks")
				self.hide()
			return True
		GObject.idle_add(watcher)
		self.refresh=watcher
	
	def queue(self, proglist):
		print("queued task")
		self.tasks.append(proglist)
		"""proglist is just a list of [downloaded,total]"""

#extra stuff from tileView's progress bar, might be useful
"""
buf=bytes()

#tracking for length
length=response.getheader('content-length')
if length:
	length=int(length)
	progress=[0, length]
	#progressbar.queue(progress)
	blocksize=max(4096, length//100)
else:
	progress=None
	blocksize=4096

while True:
	read=response.read(blocksize)
	if read:
		buf+=read
		
		if progress:
			progress[0]=len(buf)
	else:
		if progress:
			progress[0]=progress[1]
		break;
loader.write(buf)
"""

class postView(Gtk.Box):
	"""settings and stuff"""
	def __init__(self, booruWidget):
		"""set everything up"""
		super(postView, self).__init__(orientation=Gtk.Orientation.VERTICAL)
		
		#comments, tags, and sources
		#TODO: implement
		
		#web view for displaying media
		self.content=WebKit.WebView()
		
		sw=Gtk.ScrolledWindow()
		sw.add(self.content)
		sw.show_all()
		
		#pull content together
		contentBox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		contentBox.pack_start(sw, expand=True, fill=True, padding=0)
		contentBox.show()
		
		#pack everything into a neat box
		self.pack_start(contentBox, expand=True, fill=True, padding=0)
		
		#set up bottom utility bar
		backbtn=Gtk.Button(stock='gtk-go-back')
		backbtn.set_image(Gtk.Image(stock="gtk-go-back"))
		backbtn.connect("clicked", lambda btn:booruWidget.closeImage())
		
		#TODO: make this accept a "target", switch should hide/show the target
		def makeToggle(name):
			frame=Gtk.Frame(label=name)
			button=Gtk.Switch()
			frame.add(button)
			return (frame, button)
		
		(tagframe, self.tagSwitch)=makeToggle("Tags")
		(commentframe, self.commentSwitch)=makeToggle("Comments")
		(sourceframe, self.sourceSwitch)=makeToggle("Source")
		
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
