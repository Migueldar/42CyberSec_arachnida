import requests as req
from bs4 import BeautifulSoup as bs
import argparse
import threading
import atexit
#handle 429 exception (too many requests)

already_visited=set()
already_downloaded=set()

def exit_print():
	print(f"Pages visited: {len(already_visited)}")
	print(f"Images downloaded: {len(already_downloaded)}")

def parse():
	parser = argparse.ArgumentParser(
		prog = './spider', 
		description = 'scrape images from URL'
	)
	parser.add_argument('URL', help='URL to scrape')
	parser.add_argument('-r', action='store_true', help='recursive scraping, recommended use with -l', default = False)
	parser.add_argument('-l', help ='specify how many levels of recursive search (default is 1), if used without -r its ignored', default = 0)
	parser.add_argument('-p', help='specify path where images are saved (default is ./data)', default='./data')
	parser.add_argument('-o', action='store_false', help='go thorugh the web, but not out of it , for this option its important to start the url with "https://www"', default = True)
	args = parser.parse_args()
	return args.__dict__

def url_converter(base_url, url):
	if (url.startswith("//")):
		url = "https:" + url
	elif (url.startswith("/")):
		url = base_url + url
	return url

#handle xlink:href
def recursive_main(url, depth):
	already_visited.add(url)
	print(url)
	print(f"Depth: {depth}")
	try:
		response = req.get(url, timeout = 2)
		print(f"Response: {response.status_code}")
		print()
	except Exception:
		print("Couldnt open url")
		print()
		return
	if (response.status_code != 200):
		return
	try:
		soup = bs(response.content, "lxml")
	except:
		return
	threading.Thread(target=download_images(url, soup))
	if (depth >= level):
		return
	links_html = soup.find_all('a')
	for link_html in links_html:
		try:
			real_url = link_html['href']
		except Exception:
			pass
		else:
			real_url = url_converter(url, real_url)
			if (real_url.startswith(cant_exit_url) and not already_visited.__contains__(real_url)):
				recursive_main(real_url, depth + 1)

def valid_image(url):
	return url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".png") or url.endswith(".gif") or url.endswith(".bpm") 

#handle image icons tags
def download_images(url, beautiful):
	images_html = beautiful.find_all('img')
	for image_html in images_html:
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
							if len(src) > 255:
								src = src[-255:-1] + src[-1]
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
	global level, path, cant_exit_url
	cant_exit_url = ""
	url = dict.get('URL')
	recursive = dict.get('r')
	level = int(dict.get('l'))
	if not recursive:
		level = 0 
	if recursive and level == 0:
		level = 1 
	path = dict.get('p')
	out = dict.get('o')
	if not out:
		splitted = url.split('/')
		cant_exit_url = splitted[0] + "//" + splitted[2]
	recursive_main(url, 0)
