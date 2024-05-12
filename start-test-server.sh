docker build -t $IMAGE_NAME .
docker run --rm -p 8001:8000 --env ENV=test $IMAGE_NAME
