# hm-fastapi-app
Have Docker installed on your system - for windows go to
https://www.docker.com/
and download Docker Desktop for windows.
Durig installation follow the instructions (enable virtualization on your system etc).

### How to run fastapi-app
1. Clone this repository to location of your choice.
2. In command line navigate to the chosen location.
3. Build an image for fastapi application by typing:
```
docker build -t hm-fastapi-app .
```
4. Run the container by typing:
```
docker run -d -p 8000:8000 hm-fastapi-app
```
Please note, that if you choose different port, websocket functions will not work due to the fact that port 8000 is hardcoded.  

5. Go to your browser and type
```
127.0.0.1:8000/docs to list endpoints for the application
```
6. Go to your browser and type
```
http://127.0.0.1:8000/ws/orders
```
You can do that on two different tabs (or more) to see that after clicking at "Execute random orders" button, id and status (EXECUTED) will be shown to all the users (on all tabs).
7. Go to your browser and type
```
http://127.0.0.1:8000/
```
You can again, go to that url on multiple tabs.
Stoks and Quantity inputs are prefilled (so I did not have to type that during tests). You can click on a button "Place order" to see that all the users will be notifed about order placement. 

### How to run tests:
1. In the location where you cloned the repository build an image using DOckerfile.tests for fastapi application tests by typing:
```
docker build -t hm-fastapi-tests -f Dockerfile.tests .
```
2. Run the tests by typing:
```
docker run --network host hm-fastapi-tests
```
After tests are completed you can download the report.html from the container by typing:
```
docker cp <CONTAINER_ID>:/app/report.html "$(pwd)/report.html"
```
You can find <CONTAINER_ID> by typing:
```
docker ps -a
```
