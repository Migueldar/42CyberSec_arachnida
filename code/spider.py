import requests as req
from bs4 import BeautifulSoup as bs
import argparse
import threading
import atexit
#think about multiThreading req

already_visited=set()
number_images=0
number_pages=0
already_downloaded=set()

def exit_print():
	print("Images: " + str(number_images))
	print("Pages: " + str(number_pages))

def parse():
	parser = argparse.ArgumentParser(
		prog = './spider', 
		description = 'scrape images from URL'
	)
	parser.add_argument('URL', help='URL to scrape')
	parser.add_argument('-r', action='store_true', help='recursive scraping, recommended use with -l', default = False)
	parser.add_argument('-l', help ='specify how many levels of recursive search (default is 1), if used without -r its ignored', default = 0)
	parser.add_argument('-p', help='specify path where images are saved (default is ./data)', default='./data')
	parser.add_argument('-o', action='store_false', help='go thorugh the web, but not out of it (for example, if you dont want to jump from google.com to wikipedia.org and just leave the webscraping in google itself)', default = True)
	args = parser.parse_args()
	return args.__dict__

def url_converter(base_url, url):
	if (url.startswith("//")):
		url = "https:" + url
	elif (url.startswith("/")):
		url = base_url + url
	return url

#handle -o flag
#handle xlink:href
def find_links(beautiful, depth, url):
	global number_pages
	number_pages += 1
	print(depth)
	already_visited.add(url)
	download_images(url, beautiful)
	if (depth < level):
		links = beautiful.find_all('a')
		for link in links:
			try:
				real_link = link['href']
			except Exception: 
				pass
			else:
				real_link = url_converter(url, real_link)
				print(real_link)
				if (not already_visited.__contains__(real_link)):
					try:
						re = req.get(real_link, timeout = 2)
						print(re.status_code)
					except Exception: 
						pass
					else: 
						if (re.status_code == 200):
							soup = bs(re.content, "lxml")
							find_links(soup, depth + 1, real_link)

def valid_image(url):
	return url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".png") or url.endswith(".gif") or url.endswith(".bpm") 

#image tag
#icons tags
def download_images(url, beautiful):
	images_html = beautiful.find_all('img')
	for image_html in images_html:
		global number_images
		number_images += 1
		try:
			src = image_html['src']
		except:
			pass
		else:
			src = url_converter(url, src)
			if (not already_downloaded.__contains__(src)):
				already_downloaded.add(src)
				if (valid_image(src)):
					try:
						image = req.get(src, timeout=2)
					except Exception:
						pass
					else:
						if (image.status_code == 200):
							try:
								with open(path + '/' + src.replace('/','|'), "wb") as file:
									file.write(image.content)
							except MemoryError:
								print("You ran out of memory!")
								exit()
							except Exception:
								print("Couldnt download image from " + src)

if __name__  == "__main__":
	atexit.register(exit_print)
	dict = parse()
	global recursive, level, path, out, url
	url = dict.get('URL')
	recursive = dict.get('r')
	level = int(dict.get('l')) 
	if recursive and level == 0:
		level = 1 
	path = dict.get('p')
	out = dict.get('o')
	r = req.get(url)
	beautiful = bs(r.content, "lxml")
	find_links(beautiful, 0, url)
