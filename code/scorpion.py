from PIL import Image
from PIL.ExifTags import TAGS
import argparse

def parse():
	parser = argparse.ArgumentParser(
		prog = './scorpion', 
		description = 'get image metadata'
	)
	parser.add_argument('IMAGE1')
	parser.add_argument('IMAGE2', nargs='*')
	args = parser.parse_args()
	return args.__dict__

if __name__ == "__main__":
	dict = parse()
	image_path_list = list()
	image_path_list.append(dict.get('IMAGE1'))
	image_path_list += dict.get('IMAGE2')
	print(image_path_list[0])
	for img_path in image_path_list:
		img = Image.open(img_path)
		print(f"{'Name:':25}: {img.filename}")
		print(f"{'Size:':25}: {img.size[0]}, {img.size[1]}")
		exifdata = img.getexif()
		for tagid in exifdata:
			try:
				tagname = TAGS.get(tagid)
				value = exifdata.get(tagid)
				print(f"{tagname:25}: {value}")
			except Exception:
				print(f'Tag id {tagid} not found in database')
		print()
