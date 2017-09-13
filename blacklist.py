#!/usr/bin/python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

defText="""#globally blacklisted tags go here
#blank lines and lines beginning with # are ignored
#separate each blocked query with a newline
#place multiple tags on one line to block both
#negation is supported

#for example, to block any posts containing tag1 or tag2:
#tag1
#tag2

#to block posts containing BOTH tag1 AND tag2:
#tag1 tag2

#to block posts that dont contain tag1:
#-tag1

#to block posts that contain tag1, unless tag2 is also present
#tag1 -tag2

#as many tags as needed can be placed on a line
"""

blacklist=[]
default_file="blacklist.txt"

def load():
	global blacklist
	try:
		with open(default_file) as f:
			blacklist=[line.lower().split() for line in f if line.strip() and not line.strip().startswith("#")]
	except FileNotFoundError:
		print(default_file,"not found, creating")
		with open(default_file, 'w') as f:
			f.write(defText)
	
try:
	load()
except:
	print("error loading from {}, skipping".format(default_file))

editor=Gtk.TextView()
edWin=Gtk.Window()
def assemble():
	def close():
		edWin.hide()
		return True
	def submit():
		#write out the buffer
		tbuffer=editor.get_buffer()
		
		with open(default_file, 'w') as f:
			f.write(tbuffer.get_text(tbuffer.get_start_iter(), tbuffer.get_end_iter(), True))
		#reload the blacklist
		load()
		#do anything in the normal close function
		close()
	
	submitbtn=Gtk.Button("Submit")
	submitbtn.connect("clicked", lambda b:submit())
	closebtn=Gtk.Button("Cancel")
	closebtn.connect("clicked", lambda b:close())
	
	buttonbar=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
	buttonbar.pack_start(Gtk.Fixed(), expand=True, fill=True, padding=0)
	buttonbar.pack_start(submitbtn, expand=False, fill=False, padding=0)
	buttonbar.pack_start(Gtk.Fixed(), expand=True, fill=True, padding=0)
	buttonbar.pack_start(closebtn, expand=False, fill=False, padding=0)
	buttonbar.pack_start(Gtk.Fixed(), expand=True, fill=True, padding=0)
	
	sw=Gtk.ScrolledWindow()
	sw.add(editor)
	
	mainbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	mainbox.pack_start(sw, expand=True, fill=True, padding=0)
	mainbox.pack_start(buttonbar, expand=False, fill=True, padding=0)
	
	edWin.set_title("Blacklist")
	edWin.add(mainbox)
	edWin.resize(640, 720)
	edWin.connect("delete-event", lambda w, e:close())
assemble()

def gui_edit():
	"show a gui for editing the blacklist"
	print("showing blacklist gui")\
	
	with open(default_file) as f:
		editor.get_buffer().set_text(f.read())
	
	edWin.show_all()

def is_blocked(tagstr:str):
	tags=tagstr.lower().split()
	
	def testtag(block_item):
		block_item=block_item.strip()
		negated=block_item.startswith('-')
		block_item=block_item[1:] if negated else block_item
		
		#if negated, then tags MUST have the item, blacklist if it doesnt
		#if not negated, then tags must NOT have the item, blacklist if it does
		#item in tags	|	negation	|	should blacklist
		#		0		|		0		|		0
		#		0		|		1		|		1
		#		1		|		0		|		1
		#		1		|		1		|		0
			
		return negated != (block_item in tags)
	
	for blocked in blacklist:
		#if all blocked tags on this line match the tag list
		if all(map(testtag, blocked)):
			return True
	return False

if __name__=="__main__":
	def runTest(tags, blocked):
		isblock=is_blocked(tags)
		print("{} - tags: '{}' blocked? got: {} should be {}".format("PASS" if isblock==blocked else "FAIL", tags, isblock, blocked))
	
	blacklist="""a b
	c
	d -e
	-f
	"""
	blacklist=[line.split() for line in blacklist.splitlines() if line.strip() and not line.strip().startswith("#")]
	
	print(blacklist)
	
	print("\nf must be present")
	runTest("", True)
	runTest("q", True)
	runTest("asssasssfasf aa a agggg", True)
	
	print("\na and b should be blocked even if caps")
	runTest("A B", True)
	
	print("\na or b by themselves should not block, but together should")
	runTest("f sadf ndndn wwwwww", False)
	runTest("f sadf ndndn a wwwwww", False)
	runTest("f sadf ndndn b wwwwww", False)
	runTest("f b a wwwwww", True)
	
	print("\nc should always block")
	runTest("f c wwwwww", True)
	
	print("\nd is blocked if e is not present")
	runTest("f d wwwwww", True)
	runTest("f d e wwwwww", False)
	
	print("\nif the blacklist is empty, anything should pass")
	blacklist=[]
	runTest("a b c d e", False)
	runTest("asd fa ss aa", False)
	runTest("a", False)
	runTest("", False)
