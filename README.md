#### Postgres Branch notes
To use heroku, you have to:

- Download the [Heroku CLI](/https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
- Create a heroku dev account if you don't already have one
- give email to me, so you can be added as a contributor
- Use the following commands to set the DATABASE_URL enviroment variable
    - Windows CMD: ``FOR /F "usebackq delims=" %i IN (`heroku config:get DATABASE_URL -a ice2meetu`) DO set DATABASE_URL=%i``
    - bash: `DATABASE_URL=$(heroku config:get DATABASE_URL -a ice2meetu)`

# Project Proposal

#### Project Title
Ice2MeetU

#### Date
09/04/2018

#### Team Members
Kevin Cybura , Dandan Lin,  Silvena Chan, Kristoff Campbell

#### Introduction
Ice2MeetU is a group game app designed for events or parties that need a way to break the ice. The app will pair users to play a quick, randomized game. Break out our web or mobiles apps and play a game to introduce yourselves to each other in a non awkward way. 

#### Features
- An organizer can create an Event and invite people into it (similar to a slack workspace), and each event can divided the people into separate groups.
- Chat: Each event will have its own chat and each group will have its own private chat.
- Accounts:
    - Organizer accounts: choose available games, create groups, user profile fields, etc.
    - User auth: each user must create their own account with profiles
- Group people by similar interest (Ex: if you’re at a hackathon group by programming language).
- Randomized games.
- Instant chatting 
- Follow up/Connect after the meetup

#### Client/Server architecture
Need to create a rest api that can communicate with a database to implement chat, user auth, and create the “Events”. Each client(web frontend) will give the user a way to communicate to the rest api (Ex: create an account, login, chat).

#### Privacy/Security:
Need to securely store the user information for user auth. Prevent people from executing code through chat.

#### Test plan 
- Unit Test
- Performance Test
- User Studies
