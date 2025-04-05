docker  ps -- running processes/containers - container is a process with a OS, all the packages and app files 
docker stop <container-name>
docker images / docker image ls
docker build -t <image-name> <directory-of-Dockerfile>

docker build -t <image-name>:<tag> <path-of-Dockerfile>	

tag is say version

docker build -t myapp:1.0 .

Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/images/json": dial unix /var/run/docker.sock: connect: permission denied


docker pull <image-name>
docker run <image-name>

docker ps -a -show stopped containers as well show all containers which are running or not running

docker run -it <image-name> - run an image and interact with it or run an image interactively

docker run -d <iamge-name> - run the image in a detached mode that means we can exit the terminal and container will keep running in background - to create a new container from the image

docker stop <id-of-container> - to stop the running container
docker start <id-of-container> - to start the created container - to restart stopped container 

docker run -p <host port>:<container-port>

docker run -p6000:6379 redis
docker run -p6000:6379 -d redis - to run in detached mode 

docker run --name <container-name-user-defined> <image-name> - to give the name to container

docker run -pPort:Port -d -e ENVIRONMENT_VARIABLE=value --name <container-name> --network/--net <network-name> <image-name>  

ex - docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=password -name mongodb --net mongo-network mongo
docker run -d -p8081:8081 ME_CONFIG_MONGODB_ADMINUSERNAME=admin -e ME_CONFIG_MONGODB_ADMINPASSWORD=password --NET mongo-network -e ME_CONFIG_MONGODB_SERVER=mongodb mongo-express

by default any container of same app but with different versions have similar ports as in case of redis both listens to port 6379 but as they are not binded with the host's port or the port binding between the host and container is not performed they are not creating a conflict but to make any container interact with localhost we need to define port binding done by above command

docker logs <container-id>

docker logs <container-name>

docker logs <container-name> | tail - to display the last part of the logs

docker logs <container-name> -f - to stream the logs, on the go shows the logs whatever the changes are being made in the logs


docker exec -it <container-id/container- >  /bin/bash - /bin/bash to get the sheel - to get the terminal of the running container in interactive mode
type exit to come out of the terminal

/bin/sh - to get the terminal

docker network concept - 
isolated docker network - if two docker containers are running in the same docker network, they need not to have to connect using localhost:port they can directly connect with container name
but if some application is lying outside the container and they need to interact with the application that are there in the docker container then we need to interact using localhost:port

docker network ls - list of automatically generated docker networks

docker network create <network-name>
docker network create mongo-network



#commands
## create docker network
docker network create mongo-network
## start mongodb
docker run -d\
-p 27017:27017\
-e MONGO_INITDB_ROOT_USERNAME=admin\
  MONGO_INITDB_ROOT_PASSWORD=password\
--net mongo-network\
-e
--name mongodb\
mongo
## start mongo-express
docker run -d\
-p 8081:8081\
-e ME_CONFIG_MONGODB_ADMINUSERNAME=admin\
  ME_CONFIG_MONGODB_ADMINPASSWORD=password\
-e ME_CONFIG_MONGODB_SERVER=mongodb\
-e
--net mongo-network\
--name mongo-express\
mongo-express

docker compose - 
for automated way to take all the commands to run docker containers that are interconnected with each other and then map it into a file 

version: '3' - latest version of docker compose
services: - list of containers that we need in our application
	mongodb : container-name
		image:mongo
		ports:
			- 2
version:'3'
services:
 mongodb:
   image:mongo
   ports:
    - 27017:27017
   environment:
     - MONGO_INITDB_ROOT_USERNAME=admin
 	 - MONGO_INITDB_ROOT_PASSWORD=password
 mongo-express:
 image:mongo-express
 ports:
  -8080:8080
 environment:
    - ME_CONFIG_MONGODB_ADMINUSERNAME=admin
    - ME_CONFIG_MONGODB_ADMINPASSWORD=password
    - ME_CONFIG_MONGODB_SERVER=mongodb

docker compose will create the network by the help of which these containers interact with each other
it takes care of creating a common network 

docker-compose -f <yaml-file-name> <action>

-f - f flag stands for file

action - what we want to do with the container defined in the .yaml file

docker-compose -f mongo.yaml up
docker-compose -f mongo.yaml down - removes the contai ners and networks created as well

docker volumes - used for data persistency when the container restarts
In order to build a docker-image from an application we need to copy artifact / the contents of that application (jar,war,bundle.js) into Docker File 

Dockerfile is theblueprint for building the image

FROM <image-name> -Start by basing it on another image - whatever image you're building you always want to base it on another image - basing means we're gonna have that image installed inside of our image

ENV - Optionally define environmental variables - 

ENV MONGO_DB_USERNAME=admin\
   MONGO_DB_PWD=password

RUN - execute any command

RUN mkdir -p /home/app

COPY - executes on the host!
we can execute copy command with run as well but there is a problem that command would run inside the container but we want to copy files from host to container so we use COPY command

COPY SRC TARGET

COPY . /home/app or COPY ./app /home/app

CMD - executes an entry point linux command

CMD ["node","/home/app/server.js"]

CMD command is always one and is an entrypoint command but we can have multiple run commands inside our Dockerfile

Image Environment blueprint
install node
set MONGO_DB_USERNAME=admin
set MONGO_DB_PWD-password
create/home/app folder
copy current folder files to/home/app
start the app with:node server.js
 


Dockerfile
FROM node
ENV MONGO_DB_USERNAME=admin\
	MONGO_DB_PWD=password
RUN mkdir -p/home/app
COPY/home/app
CMD["node","server.js"]
blueprint for building the image

Image Layers
    app:1.0
 node:13-alpine   FROM node:13-alpine

  alpine:3.10     FROM alpine:3.10

Start"my-app"container to verify:
>app starts successfully
>app environment is configured correctly

docker ps -a | grep my-app

docker rm <container-id> 
docker rmi <image-id>

in order to delete the image you first need to stop and remove the container

in aws ecr - elastic container registry 
we can create only 1 image inside a repository
you can store different versions/tags of the same image can be stored inside a repository

You always have to login to the private repo = docker login

docker login - command to autheticate yourself on the private repository 

Pre-Requisites:
1)AWS Cli needs to be installed
2)Credentials configured

$(aws ecr get-login --no-include-email --region eu-central-1) - provided by aws to autheticate in local in background uses docker login
 
docker build -t my-app

docker tag my-app:latest 664574038682. dkr.ecr.eu-central-1.amazonaws.com/my-app:latest

Push commands for my-app
  Use the AWS CLI:
  $(aws ecr get-login --no-include-email --region eu-central-1)
  Note:If you receive an"Unknown options:--no-include-email"error when using the AWS CLI,ensure that you have the latest version
  installed.Learn more
2. Build your Docker image using the following command.For information on buildingaDocker file from scratch
  see the instructions here.You can skip this step if your image is already built:
  docker build -t my-app.
3. After the build completes,tag your image so you can push the image to this repository:
  docker tag my-app:latest 664574038682. dkr.ecr.eu-central-1.amazonaws.com/my-app:latest
4. Run the following command to push this image to your newly created AWS repository:
  docker push 664574038682. dkr.ecr.eu-central-1.amazonaws.com/my-app:latest

Image Naming in registry
registryDomain/imageName:tag
In DockerHub:
 cdocker pull mongo:4.2
 docker pull docker.io/library/mongo:4.2

 In AWS ECR:
  docker pull 520697001743.dkr.ecr.eu-central-1.amazonaws.com/my-app:1.0

  docker tag - rename the image

  docker volumes is used for state persistance in docker

If we have a host which has a database container so the data in the container is stored in the virtual file system /var/lib/mysql/data 

so when we restart or remove the container, the data is gone and it always starts from a fresh state

on the container we have virtual file system - /var/lib/mysql/data and on host we have physical file system - /home/mount/data
with the help of docker volumes we plug the physical file system along with the container's virtual file system path

Folder in physical host file system is mounted into virtual file system of Docker

If the container writes the file onto it's virtual file system then it get's replicated onto the host's file system automatically and vice versa, if we have changed something onto host's file system it gets changed onto container's file system as well.
If the container is restarted, it get's data from the host file system

3 Docker Volume Types:

- Host Volumes - We define connection between host directory and container's directory
you decide where on the host's file system that reference is made or which folder you mount into the container's system or where data gets stored

docker run -v <host-directory>:<container-directory>
docker run -v /home/mount/data:/var/lib/mysql/data

Anonymous Volumes - because you don't have a reference of automatically generate path on host
docker run -v <container-directory>
docker run -v /var/lib/mysql/data
host diectory is automatically created by docker under /var/lib/docker/volumes/random-hash/_data

- Named Volumes 

reference the volume just by names
docker run -v name:/var/lib/mysql/data 

docker volumes in docker-compose 

Named Volume

mongo-docker-compose.yaml

version : '3'
services:
  mongodb:
    image:mongo
    ports:
      - 27017:27017 
    volumes:
    - db-data:/var/lib/mysql/data

      <name>
  mongo-express:
    image: mongo-express

    ...
volumes: - list all volumes you've defined and want to mount into the container
  db-data:
    driver: local   
  benefit is you can reference that volume to some other container, useful in the case when they're sharing data

  deploying on dev -server

  in docker-compose.yaml

  services:
    my-app:
      image: private_repo/image-name:tag
      ports:
        - 3000:3000


  do a docker login, if we're fetching a private docker repository while configuring application on dev server

docker-compose file would be used on the server to deploy all the appllication/services

create a .yaml file on the dev server and paste the commands that you would want to define


docker volumes path in linux - /var/lib/docker/
volumes

docker for mac creates a linux virtual machine and stores all thr docker data here! 

Docker

- Containers, isolated env for app
- Automated Building and deploying applications : CI
- Container platform for configuring, building and distributing containers 


Kubernetes

- Infrastructure for managing multiple containers
- Automated scheduling and management of deployed application containers
- Ecosystem for managing a cluster of Docker containers

Use Official Docker Images as Base Image
- you will specific image build 

Use Specific Image Versions 

FROM node -> it will fetch latest image
  - You might get different docker image versions
  - Might break stuff
  - Latest tag is unpredictable
FROM node:17.0.1 -> Fixate the version
The more specific, the better 

Use Small-Sized Official Images
  Based on your need OS images - (Could be based on full-blown OS)
    - System Utilities packaged in 
      - Larger Image Size
    - Many OS features your image will never use
    - Otherwise will end up with Larger Images Size with lot s of utilities and packages installed.
    - OS with lots of utilities and packages installed have more known secuirity vulnerabilities which introduces unnecessary secuirity issues from the beginning
    FROM node:17.0.1
  Use Leaner OS Distro (Use Image based on a leaner and smaller OS Distro)
    - Only bundle necessary utilities (e.g Busybox instead of GNU Core Utils)
    - Minimize attack surface and build more secure image
    - Less Storage Space on Repository and Deployment Server
    - Transfer Images Faster when pulling and pushing from the repository
    - 
    FROM node:17.0.1-alpine
    - alpine lightweight Linux distro
    - secuirity-oriented 
    If you don't require any specific utilities choose leaner and smaller image 
Optimize Caching Image Layers

- Docker Images are built based on a Dockerfile
- In Dockerfile, each command creates an image layer
- to see an image layer in docker hub image go to docker hub that image and check for layers

docker history <image-name:tag> - to see the image layers  

- Docker caches each layer, saved on local filesystem
- So when you rebuild the image, if nothing has changed in a layer (or any layers preceding it), it will be re-used from cache, to build the image
- Faster image building
- Downloading only added layers
- While pulling and pushing image layers, only that layer which is changed will be downloaded, rest will be picked up from the local cache
- Once a layer changes, all following layers (downstream layers ) are re-created as well / change the content in one of image layers, all the layers downn the line will be invalidated and busted, so each from that line will be rebuild in the cache

Optimize caching for "npm install" layer
- Do not re-run : when project files changes
- re-run : when package.json file changes, so when this file changes npm install will run and after that copy mypp /app command will run so that any code changes will not make this npm install re-run

- Order Dockerfile commands from least to most frequently changing 
  - to take advantage of caching
  - faster image building and fetching

- When we build the image, we don't need everything inside the Docker image
  - autogenerated folder like target, build
  - READme files
in order to reduce image size, to prevent unintended secrets exposure

Use .dockerignore to explicitly exclude files and folders

- Create .dockerignore file in the root directory
- List files andgit and folders you want to ignore
- Matching is done using Go's filepath.Match rules

```# ignore .git and .cache folders
.git
.cache

# ignore all markdown files (md)

*.md

# ignore sensitive files

private.key
settings.json
```

There are contents that you need for building the image
but you don't need them in the final image to run the app

while building the image from a Dockerfile many artifacts are created that are generated that are required in build time such as development tools, build tools, test dependencies, temporary files

results in - increased image size
            - increased attack surface

Ex - Dependencies File such as package.json, pom.xml
- specifying project dependencies
- needed for installing dependencies
- not needed for running the app, once the dependencies are installed

building java app

- jdk is needed to compile java source code
- not needed to run Java application
- java build tools (maven, gradle) for building the application
- not needed to run Java application

How do we exclude the build dependencies from the final image?

Make use of Multi-Stage Builds

- It allows you to use temp images during the build process but keep the latest image as final artifact

ex - Dockerfile with 2 Build Stages

```
# Build Stage 1st Stage

FROM maven AS build
WORKDIR /app
COPY myapp /app
RUN mvn package

#Run stage

FROM tomcat
COPY --from=build /app/target/file.war /usr/local/tomcat/

- You can name your stages with "AS <name>"
  - 1st stage - Builds Java app
- Each FROM instruction starts a new build stage
- You can seletively copy artifacts from one stage to another
- Leaving everything behind you don't want in the final image

Only the last Dockerfile commands are the image layers


```


```
When we create an image and run it as container
Which OS user will be used to start the application?

By default Docker uses the root user
few use case, where the contqainer needs to run as root user
secuirity bad practice - container could potentially have root access on the Docker host
easier privilege escalation for an attacker

Use the Least Privileged User
- Create a dedicated user and group
- Don't forget to set required permissions
- Change to non-root user with USER directive

# create group and user

RUN groupadd -r tom && useradd -g tom tom

# set ownership and permissions
RUN chown -R tom:tom /app

# switch to user
USER tom

CMD node index.js 

- Some Base images have a generic user bundled in
- No need to create yourself
- node image - user node

```

```
Scan Your Images for Vulnerabilities
How to validate the built Image for secuirity vulnerabilities?
- scan your image for secuirity vulnerabilities
- using docker scan command
  docker scan myapp:1.0
  you need to logged in to docker hub to scan images
  docker login
- docker uses Snyk service for the vulnerability scan
- scan uses database of vulnerabilities which gets constantly updated
- scan using CLI
- scan using Docker hub
  - Triggers scan automatically when image gets pushed to the Dokcer repo
  - View the scan summary via Docker Hub or Dokcer Desktop
- Integrate in CI/CD 

```
```
8 Best Practices
1. Use Official Docker Images as Base Image
2. Use Specific Image Versions
3. USe Small-Sized Official Images
4. Optimize Caching Image Layes
5. Use .dockerignore to exclude files and folders
6. Make use of "Multi-Stage Builds"
7. Use the Least Priviledged User
8. Scan Your Images for Vulnerabilities


```