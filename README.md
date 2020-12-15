# querido-diario-toolbox

## Prepare devilment environment
Before start to code you need to setup the development environment. This 
project uses python virtual environment to isolate the python libraries. 
Some Java library (e.g. Apache Tika and Tabula) are also needed. 
So, to get everything you need,  run:

```
make setup
```

This command will create the python virtual environment, install python libraries
and download the necessary binaries. 

Remember to activate the python env before start your development:

```
source .venv/bin/activate
```

## How to run the tests

Once you have your env set up. You can run the tests:

```
make tests
```

