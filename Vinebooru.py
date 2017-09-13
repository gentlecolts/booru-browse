from pyquery import PyQuery as pq
from urllib.parse import quote
from pprint import pprint
import re

baseurl='https://booru.vineshroom.net'
thumbsrc=re.compile(r'src="(\/_thumbs\/[0-9a-f]+\/thumb\.[a-z]+)"')

def getChildrenText(tag, childtag):
	"""returns the text of all children of tag which are <childtag>"""
	tags=[]
	for child in tag:
		if child.tag==childtag:
			tags.append(child.text)
	return tags

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
		query=pq(url=searchurl)
		posts=query('a.thumb')
		
		#print(type(posts))
		results=[]
		for tag in posts:
			id=tag.attrib['data-post-id']
			post={
				'id':int(id), 
				'tags':tag.attrib['data-tags'], 
				'preview_url':baseurl+tag.find('img').attrib['src'],
				'post_page_url':baseurl+tag.attrib['href'], 
			}
			post['artist']=[x for x in post['tags'].split() if x.lower().startswith("artist:")]
			
			results.append(post)
		
		#pprint(results)
		
		return results
	
	def fetchPost(self, post:dict):
		"""generate the file_url key
		
		"""
		query=pq(url=post['post_page_url'])
		#get url to post image
		post['file_url']=baseurl+query('img.shm-main-image')[0].attrib['src']
		
		#guarentee both source keys exist and fill them
		post['source']=''
		post['sources']=[]
		
		#print("gathering sources")
		#TODO: this seems to work "well enough" but really isnt a good approach
		sources=[]
		for source in query('div.blockbody tr'):
			if 'Source' in getChildrenText(source, 'th'):
				sources.append(source.find('td').find('div').find('a').attrib['href'])
		
		if sources:
			post['source']=sources[0]
			post['sources']=sources[1:]
		pprint(sources)
		#pprint(post)
		
		#TODO: gather comments
