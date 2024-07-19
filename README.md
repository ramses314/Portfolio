Hi, my name is Lev and I am a middle python developer. This is my portfolio, it consists of three projects:

<br>
<br>

<h1 align="center"> Project #01 Ticket Backend

 </h1>

<p align="center">
ticket sales web platform
</p>

<p align="center">
  <a href="#-Technology">Technology</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-AboutProject">About Project</a>&nbsp;&nbsp;&nbsp;
</p>

<br>

## 🚀 Technology

- Python
- Django
- JavaScript (+JQuery)
- HTML/CSS
- Postgres/MySQL
- sockets
- Oauth
- etc

## 💻 AboutProject

The backend for the ticket sales platform. 
Implemented:
- shopping cart
- payment
- purchase history
- registration (+ including referral links)
- oauth
- ticket booking via sockets (when choosing a numbered ticket, it becomes unavailable for selection by other users)
- customization of the django admin panel (for the associated generation of a certain number of tickets for events)
- etc

<br>

<h1 align="center"> Project #02 Aiogram Bot Constructor

 </h1>

<p align="center">
This telegram bot is the basis for the zero coding platform for creating bots
</p>

<p align="center">
  <a href="#-Technology">Technology</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-AboutProject">About Project</a>&nbsp;&nbsp;&nbsp;
</p>

<br>

## 🚀 Technology

В проекте используются следующие технологии:

- Python
- Aiogram
- Postgres
- SQLAlchemy
- Alembic
- Poetry
- etc

## 💻 AboutProject

The bot's work is based on deep interaction with the database (in particular for message texts, button texts, videos, etc.), this allows us to dynamically change the logic of the bot without getting into the code. The project implements a number of constructors that read the logic of the bot, taking into account callbacks and other parameters. This project was created for the basis of zerocoding bots, the front part is needed for full implementation.

<br>

<h1 align="center"> Project #03 Socket API General

 </h1>

<p align="center">
A server for storing information from other servers via sockets
</p>

<p align="center">
  <a href="#-Technology">Technology</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-AboutProject">About Project</a>&nbsp;
</p>

<br>

## 🚀 Technology

В проекте используются следующие технологии:

- Python
- Postgres
- FastAPI
- SQLAlchemy
- Alembic
- uvicorn

## 💻 About Project

The essence of the project and the server is to collect information from child projects, for each child project (microservice) own database. Databases are the same in structure, but differ in content. The part provided by the server collects all information via sockets. At the input, the socket receives the name of the model and the fields of the object, the server processes the information and writes it to the main database, common to all, while avoiding all collisions that may appear in this task.

---
Thank you for your time ♥ I am ready for cooperation and joint projects :wave: [my mail](https://discord.gg/rocketseat)