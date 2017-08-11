import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

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

class postView(Gtk.HBox):
	"""settings and stuff"""
	def __init__(self, booruWidget):
		"""set everything up"""
		super(postView, self).__init__()
		
