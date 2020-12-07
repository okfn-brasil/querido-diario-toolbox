# querido-diario-toolbox

## How to run the tests

In order to run the tests locally you need to install some binaries or container image or both.

## Run tests within container

To run the tests within a container you should install [podman](https://podman.io/) 
in your machine. It is used to build and run the containers. For that you can 
run the following commands:

```
make build # Build container image
make test  # Run tests
```

After you build the container image, you just need to run the `make test` every time
you want to run the tests. You just need to rerun `make build` if you change the 
`Dockerfile` of the container image. A container image is used to avoid installing 
binaries used by the project in the host machine. As well as keeping all the environment 
equal in all developers's machines.

## Run tests locally

If you do not want to run the tests using containers, you can download the binaries 
used by the project, mainly jar files, configure the tests and  run them manually.
There is a makefile target to download the binaries:

```
make download-binaries
```

The binaries will be downloaded in the `bin` directory in the root of the repository.
