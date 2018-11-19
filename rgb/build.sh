docker build -f red.Dockerfile -t space:5000/red_lantern .
docker push space:5000/red_lantern
docker build -f green.Dockerfile -t space:5000/green_lantern .
docker push space:5000/green_lantern
docker build -f blue.Dockerfile -t space:5000/blue_lantern .
docker push space:5000/blue_lantern
