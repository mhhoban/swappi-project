# Swappi: For Swapping Stuff

## Introduction:
Swappi! aims to be a simple item catalog system where people can post items
they want to swap and what they're looking to swap them for!

## Requirements:
Swappi! uses Google's OAuth 2.0 system, so users will log into Swappi! using
their gmail logins. You will also have to create web application credentials
for your Swappi! deployment. You can find instructions for doing so here:
https://developers.google.com/api-client-library/python/auth/web-app

The project is designed to work with Python 2.7 and the setup.py script uses
PIP.While running the setup script in a virtual environment is not required,
it is highly recommended.

## Setup

Run the setup script from the project's base directory with the command
```
python setup.py
```
You should then put the json secrets file you created using the instructions
in the link from the last section in the project's base directory and name it
`client_secrets.json`

After the script has finished installing the necessary packages and setting up
the database, and you have put your client secrets file in place,
you can run the project on a development server by running
```
python swappi/swappi_app.py
```
from the project's root directory, then access the web app through your browser
at `localhost:8080` .

## JSON Endpoint
In addition to viewing pages for listed items, they can also obtain a JSON endpoint
at {domain}/json-item/{item-id}

## License

Project is freely open source under the terms of the
[MIT License](http://choosealicense.com/licenses/mit/)
