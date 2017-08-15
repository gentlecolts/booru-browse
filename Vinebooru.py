from pyquery import PyQuery as pq
from urllib.parse import quote
from pprint import pprint
import re

baseurl='https://booru.vineshroom.net'

test="""
<div class="shm-image-list" data-query="search=game%3Aundertale%20streamer%3Ajoel">	<span class="thumb"><a href="/post/view/50524search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="artist:deepweeb game:tekken_7 game:undertale papyrus pizza skeletor spaghetti streamer:joel" data-post-id="50524"><img id="thumb_50524" title="artist:deepweeb game:Tekken_7 game:undertale papyrus pizza skeletor spaghetti streamer:joel // 2500x1875 // 1.4MB" alt="artist:deepweeb game:Tekken_7 game:undertale papyrus pizza skeletor spaghetti streamer:joel // 2500x1875 // 1.4MB" height="144" width="191" src="/_thumbs/33a98e120d496d7fb7e5bedf0edb3463/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/50219search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="artist:outofknives frisk game:undertale ms_paint streamer:joel" data-post-id="50219"><img id="thumb_50219" title="artist:OutOfKnives frisk game:undertale ms_paint streamer:joel // 1113x640 // 48.8KB" alt="artist:OutOfKnives frisk game:undertale ms_paint streamer:joel // 1113x640 // 48.8KB" height="110" width="192" src="/_thumbs/d09a03e4e73c164958338c5397017da5/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/49895search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="tuna_tuesday artist:deepweeb game:undertale streamer:joel undyne" data-post-id="49895"><img id="thumb_49895" title="Tuna_Tuesday artist:deepweeb game:undertale streamer:joel undyne // 900x600 // 881.4KB" alt="Tuna_Tuesday artist:deepweeb game:undertale streamer:joel undyne // 900x600 // 881.4KB" height="128" width="192" src="/_thumbs/29b7e6ace9ff95540157bc98baac5e3b/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/49876search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="artist:quill_productions game:undertale streamer:joel streamer:vinny" data-post-id="49876"><img id="thumb_49876" title="artist:Quill_Productions game:undertale streamer:joel streamer:vinny // 1920x1080 // 82.5KB" alt="artist:Quill_Productions game:undertale streamer:joel streamer:vinny // 1920x1080 // 82.5KB" height="108" width="192" src="/_thumbs/bb97ae4322828f2e4b1c0c8ecd861b3a/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/48267search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="roy artist:tetsuraryuuken computer game:kirby's_dream_course game:undertale jojo's_bizarre_adventure kirby menacing papyrus source_filmmaker streamer:joel" data-post-id="48267"><img id="thumb_48267" title="Roy artist:tetsuraryuuken computer game:kirby's_dream_course game:undertale jojo's_bizarre_adventure kirby menacing papyrus source_filmmaker streamer:joel // 1440x1800 // 2.6MB" alt="Roy artist:tetsuraryuuken computer game:kirby's_dream_course game:undertale jojo's_bizarre_adventure kirby menacing papyrus source_filmmaker streamer:joel // 1440x1800 // 2.6MB" height="192" width="153" src="/_thumbs/3613f842569fb55dc3eb0371759ab2e1/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/45584search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="game:undertale papyrus streamer:joel" data-post-id="45584"><img id="thumb_45584" title="game:undertale papyrus streamer:joel // 1800x1100 // 230.3KB" alt="game:undertale papyrus streamer:joel // 1800x1100 // 230.3KB" height="117" width="192" src="/_thumbs/d9ee228bf8cf4ac1cf1002fa34906252/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/44601search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="game:twisted_metal game:undertale streamer:joel undyne" data-post-id="44601"><img id="thumb_44601" title="game:twisted_metal game:undertale streamer:joel undyne // 1280x1024 // 188.3KB" alt="game:twisted_metal game:undertale streamer:joel undyne // 1280x1024 // 188.3KB" height="153" width="192" src="/_thumbs/75d167a5b521fd699f49e141beebf05d/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/42622search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="artist:hexxecon frisk game:undertale gun sans streamer:joel" data-post-id="42622"><img id="thumb_42622" title="artist:hexxecon frisk game:undertale gun sans streamer:joel // 561x1162 // 140.0KB" alt="artist:hexxecon frisk game:undertale gun sans streamer:joel // 561x1162 // 140.0KB" height="192" width="92" src="/_thumbs/3d34691a5c80550db6b7d2d4dc0d4f97/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/42571search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="au game:undertale streamer:joel" data-post-id="42571"><img id="thumb_42571" title="au game:undertale streamer:joel // 1500x1000 // 97.9KB" alt="au game:undertale streamer:joel // 1500x1000 // 97.9KB" height="128" width="192" src="/_thumbs/e54ab013d61f49dd5839e7a4bbaa6ce9/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/42553search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="game:undertale papyrus streamer:joel" data-post-id="42553"><img id="thumb_42553" title="game:undertale papyrus streamer:joel // 800x600 // 22.0KB" alt="game:undertale papyrus streamer:joel // 800x600 // 22.0KB" height="144" width="192" src="/_thumbs/19111d939d7d1233a6348a61d8b1a83a/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/41974search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="game:undertale papyrus streamer:joel" data-post-id="41974"><img id="thumb_41974" title="game:undertale papyrus streamer:joel // 600x451 // 118.9KB" alt="game:undertale papyrus streamer:joel // 600x451 // 118.9KB" height="144" width="192" src="/_thumbs/f5a2fa378b93eede492dff86223e8b69/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/41617search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="bad_time brown_hair eyes game:undertale glowing grand_dad granddad guitar streamer:joel vinesauce" data-post-id="41617"><img id="thumb_41617" title="bad_time brown_hair eyes game:undertale glowing grand_dad granddad guitar streamer:joel vinesauce // 1280x1024 // 437.0KB" alt="bad_time brown_hair eyes game:undertale glowing grand_dad granddad guitar streamer:joel vinesauce // 1280x1024 // 437.0KB" height="153" width="192" src="/_thumbs/da2cae02561a83b711022c5819a938e1/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/40612search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="dio game:undertale papyrus streamer:joel" data-post-id="40612"><img id="thumb_40612" title="dio game:undertale papyrus streamer:joel // 1366x728 // 1.0MB" alt="dio game:undertale papyrus streamer:joel // 1366x728 // 1.0MB" height="102" width="192" src="/_thumbs/4a2e82834323a45c4523779e0f183390/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/40160search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="artist:dullvivid creepy flower flowey game:undertale omega_flowey spooky spoopy streamer:joel thing" data-post-id="40160"><img id="thumb_40160" title="artist:dullvivid creepy flower flowey game:undertale omega_flowey spooky spoopy streamer:joel thing // 1222x806 // 2.0MB" alt="artist:dullvivid creepy flower flowey game:undertale omega_flowey spooky spoopy streamer:joel thing // 1222x806 // 2.0MB" height="126" width="192" src="/_thumbs/6f060f06f1aa1cd1dcdbd1135743885d/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/37790search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="brb game:undertale pixel_art streamer:joel" data-post-id="37790"><img id="thumb_37790" title="brb game:undertale pixel_art streamer:joel // 110x83 // 2.6KB" alt="brb game:undertale pixel_art streamer:joel // 110x83 // 2.6KB" height="144" width="192" src="/_thumbs/fbbe644f4e0478c9d8cf8f3b6609f0bd/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/37078search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="game:undertale pixel_art streamer:joel vinesauce" data-post-id="37078"><img id="thumb_37078" title="game:undertale pixel_art streamer:joel vinesauce // 91x114 // 4.6KB" alt="game:undertale pixel_art streamer:joel vinesauce // 91x114 // 4.6KB" height="192" width="153" src="/_thumbs/5600d61f4c2709db90843d0463e8f108/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/36750search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="game:undertale lunaticlunic(artist) pixel skeleton slayer sprite streamer:joel wip" data-post-id="36750"><img id="thumb_36750" title="game:undertale lunaticlunic(artist) pixel skeleton slayer sprite streamer:joel wip // 620x475 // 96.2KB" alt="game:undertale lunaticlunic(artist) pixel skeleton slayer sprite streamer:joel wip // 620x475 // 96.2KB" height="147" width="192" src="/_thumbs/92c4b54e255a152acb910e1257b737d1/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/36668search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="game:undertale sans streamer:joel traditional vinny-kun(artist)" data-post-id="36668"><img id="thumb_36668" title="game:undertale sans streamer:joel traditional vinny-kun(artist) // 1200x1800 // 466.8KB" alt="game:undertale sans streamer:joel traditional vinny-kun(artist) // 1200x1800 // 466.8KB" height="192" width="128" src="/_thumbs/599fedd6d23e7392f7a946c4c4b63812/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/36322search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="artist:neogalaxy418 death dr_pepper frisk game:undertale gore neoshroom_(neogalaxy418) streamer:joel vargshroom vineshroom" data-post-id="36322"><img id="thumb_36322" title="artist:neogalaxy418 death dr_pepper frisk game:undertale gore neoshroom_(neogalaxy418) streamer:joel vargshroom vineshroom // 2048x1152 // 477.3KB" alt="artist:neogalaxy418 death dr_pepper frisk game:undertale gore neoshroom_(neogalaxy418) streamer:joel vargshroom vineshroom // 2048x1152 // 477.3KB" height="108" width="192" src="/_thumbs/ab6556dc4b8894e89b26534d190b203a/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/35516search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="game:undertale sans streamer:joel" data-post-id="35516"><img id="thumb_35516" title="game:undertale sans streamer:joel // 720x1280 // 353.6KB" alt="game:undertale sans streamer:joel // 720x1280 // 353.6KB" height="192" width="108" src="/_thumbs/1fe267e68941188873c954384b6ffd1a/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/35510search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="6th_anniversary anniversary game:undertale sans stream streamer:joel" data-post-id="35510"><img id="thumb_35510" title="6th_anniversary anniversary game:undertale sans stream streamer:joel // 504x228 // 7.7KB" alt="6th_anniversary anniversary game:undertale sans stream streamer:joel // 504x228 // 7.7KB" height="86" width="192" src="/_thumbs/1505b609ec9838ceb3da7bc4dc3917e8/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/35485search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="game:undertale music streamer:joel undyne" data-post-id="35485"><img id="thumb_35485" title="game:undertale music streamer:joel undyne // 600x400 // 94.9KB" alt="game:undertale music streamer:joel undyne // 600x400 // 94.9KB" height="128" width="192" src="/_thumbs/23169d3986beb37aa6d1c25a09eefd05/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/35239search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="game:undertale streamer:joel streamer:vinny" data-post-id="35239"><img id="thumb_35239" title="game:undertale streamer:joel streamer:vinny // 845x601 // 117.7KB" alt="game:undertale streamer:joel streamer:vinny // 845x601 // 117.7KB" height="136" width="192" src="/_thumbs/59d71c8bcaf25eba8df75afcfa7cf8ea/thumb.jpg"></a>
</span>
	<span class="thumb"><a href="/post/view/35041search=game%3Aundertale%20streamer%3Ajoel" class="thumb shm-thumb shm-thumb-link " data-tags="arcade_madness artist:smash3dsplayer2 clay game:earthbound game:undertale ness sans streamer:joel" data-post-id="35041"><img id="thumb_35041" title="arcade_madness artist:smash3dsplayer2 clay game:earthbound game:undertale ness sans streamer:joel // 2354x1180 // 548.4KB" alt="arcade_madness artist:smash3dsplayer2 clay game:earthbound game:undertale ness sans streamer:joel // 2354x1180 // 548.4KB" height="96" width="192" src="/_thumbs/e924fa1d239a8c2789f53907ec9f675c/thumb.jpg"></a>
</span>
</div>
"""

thumbsrc=re.compile(r'src="(\/_thumbs\/[0-9a-f]+\/thumb\.[a-z]+)"')

class Vinebooru():
	"""class for specifcally vinebooru"""
	def __init__(self):
		"""open a connection to the vinebooru"""
	
	def post_list(self, tags:str, page:int=1):
		"""return a list of dicts with the query"""
		#remove excess whitespace from tags
		tags=' '.join(tags.split())
		#construct the query
		searchurl='{}/post/list/{}/{}'.format(baseurl, quote(tags), page)
		#print(searchurl)
		
		#get the stuff
		#query=pq(url=searchurl)
		query=pq(test)
		posts=query('a.thumb')
		
		print(type(posts))
		results=[]
		for tag in posts:
			#help(tag)
			id=tag.attrib['data-post-id']
			post={
				'id':int(id), 
				'tags':tag.attrib['data-tags'], 
				'preview_url':baseurl+tag.find('img').attrib['src'],
			}
			results.append(post)
		
		pprint(results)
		
		#raise NotImplementedError("not done yet")
		return results
