docker  ps -- running processes/containers - container is a process with a OS, all the packages and app files 
docker stop <container-name>
docker images / docker image ls
docker build -t <image-name> <directory-of-Dockerfile>

Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/images/json": dial unix /var/run/docker.sock: connect: permission denied


docker pull <image-name>
docker run <image-name>

docker ps -a -show stopped containers as well show all containers which are running or not running

docker run -it <image-name> - run an image and interact with it or run an image interactively

docker run -d <iamge-name> - run the image in a detached mode that means we can exit the terminal and container will keep running in background - to create a new container from the image

docker stop <id-of-container> - to stop the running container
docker start <id-of-container> - to start the created container - to restart stopped container

docker run -p<host port>:<container-port>

docker run -p6000:6379 redis
docker run -p6000:6379 -d redis - to run in detached mode 

docker run --name <container-name-user-defined> <image-name> - to give the name to container 

by default any container of same app but with different versions have similar ports as in case of redis both listens to port 6379 but as they are not binded with the host's port or the port binding between the host and container is not performed they are not creating a conflict but to make any container interact with localhost we need to define port binding done by above command

docker logs <container-id>

docker logs <container-name>

docker exec -it <container-id/container-name>  /bin/bash - /bin/bash to get the sheel - to get the terminal of the running container in interactive mode
type exit to come out of the terminal


