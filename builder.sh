docker build -t $1 .
docker run --name $2 -it -v $PWD/code:/code $1 