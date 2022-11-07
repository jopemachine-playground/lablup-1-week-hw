# lablup-1-week-hw

## Simple specification

* Multi user, Single Room chatting implementation.

* Show each user's id, chatting message, chatting datetime.

* Using Redis for maintaining user's login sessions.

* Using Mongodb for storing user's information.

* Do not keep chatting messages.

* Implemented using socket.io (Web-socket) in the server, client both side.

* Include Dockerfile, docker-compose.yml

## Set up

To run service, run below command.

```
$ docker-compose -f docker-compose-dev.yml up
```

