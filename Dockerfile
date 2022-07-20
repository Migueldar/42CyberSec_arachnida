FROM debian

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install python3 python3-pip -y
RUN pip install requests beautifulsoup4 lxml