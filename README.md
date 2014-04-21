#Cann Tables

![Screenshot](http://i.imgur.com/ndHhPAX.png)

A small flask application that displays football tables in a Cann format.

##Installation
- Clone this git repo
- Create and activate a virtualenv
- Install the requirements:

        pip install -r requirements.txt

- Run the following command to setup the database:

	    python manage.py db upgrade

- Run the scraper and the flask app:

		python manage.py scrape
		python manage.py runserver

- Run the `freeze` command to produce the .html files:

		python manage.py freeze

You can also run the following command to get an interactive shell with `app`, `db` and the `Team` and `League`
models available:

    python manage.py shell


##Deployment
You can deploy this app using dokku or heroku (untested):

- Push this repo to your dokku/heroku instance
- Set the `CANN_ENV` enviroment variable to `"prod"`
- Setup a Postgresql server
- Run the scrape command inside the instance:

        python manage.py scrape



---
Licensed under GPL v3
