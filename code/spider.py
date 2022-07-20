import requests as req
from bs4 import BeautifulSoup as bs
import argparse
import threading
#bot only valid for https pages
#ver como gestionar cosas como en.wikipedia.org
#think about multiThreading req
#add list with all links visited

def parse():
	parser = argparse.ArgumentParser(
		prog = './spider', 
		description = 'scrape images from URL'
	)
	parser.add_argument('URL', help='URL to scrape')
	parser.add_argument('-r', action='store_true', help='recursive scraping, recommended use with -l', default = False)
	parser.add_argument('-l', help ='specify how many levels of recursive search (default is 1), if used without -r its ignored', default = 1)
	parser.add_argument('-p', help='specify path where images are saved (default is ./data)', default='./data')
	parser.add_argument('-o', action='store_false', help='go thorugh the web, but not out of it (for example, if you dont want to jump from google.com to wikipedia.org and just leave the webscraping in google itself)', default = True)
	args = parser.parse_args()
	return args.__dict__

#considerar casos extraños (wikipedia links)
def find_links(beautiful, depth):
	links = beautiful.find_all('a')
	for link in links:
		real_link = link['href']
		try:
			print(real_link)
			re = req.get(real_link)
		except Exception: 
			pass
		else: 
			if (re.status_code == 200):
				soup = bs(re.content, "lxml")
				download_images(soup)
				find_links(beautiful, depth + 1)

def valid_image(url):
	return url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".png") or url.endswith(".gif") or url.endswith(".bpm") 

#./data instead of /imgaes/
def download_images(beautiful):
	images_html = beautiful.find_all('img')
	for image_html in images_html:
		try:
			src = image_html['src']
		except:
			pass
		else:
			if (valid_image(src)):
				image = req.get(src)
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
	dict = parse()
	global recursive, level, path, out, url
	url = dict.get('URL')
	recursive = dict.get('r')
	level = int(dict.get('l'))
	path = dict.get('p')
	out = dict.get('o')
	r = req.get(url)
	beautiful = bs(r.content, "lxml")
	download_images(beautiful)
	#find_links(beautiful, 0)
