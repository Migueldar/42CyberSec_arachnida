This proyect has 2 parts, spider and scorpion. Spider will scrape the web given recursively and download all the images found. Scorpion shows all the metadata of any given number of photos. I think the combination between both is obvious :). 

To install the used libraries, clone the repository and run "pip3 install -r requirements.txt"
To execute either scorpion or spider, run "python3 spider.py ..." or "python3 scorpion.py ..."

The folder in which the images go needs to be created before lauching spider.py, by default its ./data 

Lmxl instalation takes a bit, if it doesnt install, change "lmxl" in line 51 of spider for "html.parser"
