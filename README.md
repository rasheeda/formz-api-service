# formz-api-service

A simple API service for storing and retrieving JSON data in flask

I built this is part of a learning series on Flask.

Part 1: https://www.youtube.com/watch?v=88ulEksE_wM

Part 2: https://www.youtube.com/watch?v=K40H0nsw6Oo

To get this up and running:


`Cd into project folder` and run the commands below:

`pipenv shell`

`python app.py`

## API Routes
`/api/forms`
GET|POST

`api/forms/<id>`
GET|UPDATE|DELETE

`api/forms/<id>/data`
GET|POST

`api/forms/<id>/data/<id>`
GET|UPDATE|DELETE
