# Ice2MeetU: A CSCI499 Hunter Capstone Production

The Ice2MeetU project aims at the development of a web based application specially designed for events
or parties for ice breaking purpose which can greatly help individuals to open up and overcome social anxiety.

Checkout our [presentation](https://bit.ly/2EA5nTs)!

# Features
-   **Create Event**<br />
    An organizer can create an event and invite people to it (similar to a slack workspace)

-   **Join Event**<br />
    Individuals can join an existing event using associated access code

-   **Play Game with your Event!**<br />
    Start a game and once your event attendees join, they'll be randomly grouped to play a game!

-   **...Or just play games, no need to register**<br />
    Just pick the number of players and games will be generated for you.

# Test It Out
We deployed our application to Heroku, you can check it out here [Ice2MeetU](https://ice2meetu.herokuapp.com/)

## Installation

Ice2MeetU requires [Python](https://www.python.org/) and [Django](https://www.djangoproject.com/) to run.

#### Dependencies
```sh
$ cd semester-project-ice2meetu

$ pip install -r requirements.txt
```

#### Database Setup
```sh
$ pip install django psycopg2
```
Install Postgres & then setup a local Postgres Database:
* Create an admin user and password for your DB: <br />
```sh
$ createuser -P -s -e <SOME_USERNAME>
```
* Create the DB: <br />
```sh 
$ createdb -h localhost -U <USERNAME_FROM_ABOVE> <DB_NAME>
```
* Set your environment varibles
```sh
export CAPSTONE_DB=<DB_NAME>
export CAPSTONE_USER=<USERNAME_FROM_ABOVE>
export CAPSTONE_PASSWORD=<PASSWORD_YOU_SET>
```

Migrate the Database
```sh
$ cd semester-project-ice2meetu

$ python manage.py makemigrations

$ python manage.py migrate
```

Optional: Load dump data (We have five dumpdata files, make sure you are loading them in following order)
```sh
$ python manage.py loaddata db-users.json

$ python manage.py loaddata db-creation.json

$ python manage.py loaddata db-games.json

$ python manage.py loaddata db-gamestart-creation.json

$ python manage.py loaddata db-gameplay.json
```

After creating the database structure and loaded the dumpdata, we can create an administrative account by typing:
```sh
python manage.py createsuperuser
```
Before running the application, make sure you have both Postgres and Redis running, if not, start them using following two commands
```sh
$ brew services start postgresql

$ brew services start redis
```

# Running 
If you haven't started Redis above, you can also use Docker:
```sh
$ docker run -p 6379:6379 -d redis:2.8
```

Start the Django server.
```sh
$ python manage.py runserver
```
Then, navigate to following address in your preferred browser.
```sh
127.0.0.1:8000
```
# Run Tests
```sh
$ python manage.py test gameplay
```
# Accessing REST-API

Get Auth Token
```
/api-auth
```
* username and password are required to access your authtoken.
```
/api/users

/api/events

/api/games
```
* Auth token must be sent as token in the header of your request or if your accessing via the browser you can be logged in.



# Future Work
- Better Group Randomization 
 Improve group randomization for better management

- Messaging System 
Add messaging system for users to follow up with each other after event 

- EventAdmin Interface 
Add more functionalities to EventAdmin Portal 

- User Rating System 
Users can rate group members

# License

MIT

# Author
- [Campbell, Kristoff](https://github.com/kristoff-campbell28)
- [Chan, Silvena](https://github.com/silvenac)
- [Cybura, Kevin](https://github.com/KevinCybura)
- [Lin, Dandan](https://github.com/dandanlin0702)
