#!/usr/bin/python3
#import gi
#gi.require_version("Gtk", "3.0")
#from gi.repository import Gtk, GObject

blacklist=[]
default_file="blacklist.txt"

def load():
	global blacklist
	with open(default_file) as f:
		blacklist=[line.lower().split() for line in f if line.strip() and not line.strip().startswith("#")]
	
try:
	load()
except:
	print("error loading from {}, skipping".format(default_file))

def gui_edit():
	"show a gui for editing the blacklist"
	print("showing blacklist gui")

def is_blocked(tagstr:str):
	tags=tagstr.lower().split()
	
	def testtag(block_item):
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
