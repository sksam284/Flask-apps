# python redis cache

This project is for using redis as cache using python

## Project Stack

The project stack and the api response format of this microservice is in
accordance with the  micro services.
1. Python
2. Flask
3. Flask Restfull
4. Redis

The response format of the apis are as per https://jsonapi.org/ standards.

## Installation

#### Install Python 3 & Pip

Linux -

`$ sudo apt-get update`
`$ sudo apt-get install python3.6`

Windows-

Download Python 3 from https://www.python.org/downloads/ and install


#### Install Virtualenv

`$ pip install virtualenv`

`$ Set enviornment path for python, pip and virtualenv`


#### Create and activate a virtualenv for the project

`$ virtualenv venv`

Windows-

`$ venv\Scripts\activate`

Linux-

`$ source venv/bin/activate`

You should see `(venv)` added to the beginning of your Terminal input line, which indicates that the virtualenv is active.

The virtualenv must be activated during development.


#### Install Requirements

Install the Python requirements for the project

`$ pip install -r requirements.txt`


## Run the server

`$ python manage.py runserver`

The server runs at `http://localhost:6500`


## Api Docs (Swagger docs)
Api docs will be served under `http://localhost:6500/apidocs/` after running the server
