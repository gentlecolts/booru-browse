from pyquery import PyQuery as pq
from urllib.parse import quote
from pprint import pprint
import re

baseurl='https://booru.vineshroom.net'
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
		
		for source in query('div.view'):
			print('found source:',source)
			link=source.find('a').attrib['href']
			
			target='sources' if post['source'] else 'source'
			post[target]+=link
		
		#TODO: gather comments
