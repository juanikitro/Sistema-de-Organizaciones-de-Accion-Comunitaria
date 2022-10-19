# Sistema-de-Organizaciones-de-Accion-Comunitaria

## Usage

The system is a CRUD where the principal entity is the ORGANIZATION.
Some functions of the system are:
- Create and follow the states of a org.
- Upload and replace the org documentation.
- Create users with differents permissions.
- Comunicate with another user or organization.
- Schedule the org documentation expiration.
- Organicze activities, events and visits in 3 calendars.
- Do claims about an org.
- More...

## Why?

This is my bigger real project. The goal was to create a system that will help "General Directorate of Community Relations" to organize the actions of the community.

This is my first and my last Django project for the moment.

I want to public it because I enjoied a lot doing it and I am not working more for the government, so I can, but you can't view the deployed version because is private.

## What is SOAC?

The System of Community Action Organizations (SOAC) has as its main objective to store community action organizations, registered and unregistered, along with their status, documentation, information and visits in order to be able to apply follow-up through multi-filter searches, give registration, cancellation and modification of organizations (Registered and not registered in ROAC), view and modify their status, information and documentation and download all available data.

## Complete algorithm
![SOAC algorithm](https://raw.githubusercontent.com/juanikitro/Sistema-de-Organizaciones-de-Accion-Comunitaria/main/Algoritmo.drawio.png)

## Database design

The database consists of 5 entities:
The “organizations” are the main entity in the system, that is why the rest of the entities are connected to them. Each organization may count, not necessarily, with "visits". These visits will be created by “users”, who connect to the organizations. Every time a user creates, deletes or modifies an organization or visit, this action triggers a "notification" which is saved in the "history" in order to have a record of what happens in the system.

![SOAC DB](https://raw.githubusercontent.com/juanikitro/Sistema-de-Organizaciones-de-Accion-Comunitaria/main/Dise%C3%B1o%20de%20la%20DB.drawio.png)

---

# Set Up

## Clone repo and enter

```bash
git clone https://github.com/juanikitro/Sistema-de-Organizaciones-de-Accion-Comunitaria.git
```

```
cd Sistema-de-Organizaciones-de-Accion-Comunitaria
```

---

## VENV (Linux)

### Create

```
python -m venv venv 
```

### Enter

```
source venv/bin/activate
```

### Install requeriments

```
pip install -r requirements.txt
```

### Templates
You need to build all the templates you need.

### Run a test 

```
python ./manage.py runserver
```
