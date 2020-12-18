# querido-diario-toolbox

The goal of the `querido-diario-toolbox` is give the Querido Diário 
community the building blocks to perform its own analyses and manipulation in 
the data extracted by the Querido Diário project.  The lib should empowers the 
production applications used by the Querido Diário project to process the data 
as well as any other people which wants to perform their own analyses and 
run scripts. 

For that, the lib is expected to give bunch of different level of abstractions
to work with the data. From simple text extraction from strings as well as 
wrapper around APIs, etc.[201~]]

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

