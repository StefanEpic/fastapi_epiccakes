## 👾 RSHB Game API
![FastAPI](https://img.shields.io/badge/FastAPI-blue)
![Gunicorn](https://img.shields.io/badge/Gunicorn-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue)
![Nginx](https://img.shields.io/badge/Nginx-green)
![Docker](https://img.shields.io/badge/Docker-blue)

АPI for RSHB Bank's browser game

<img src="https://github.com/StefanEpic/fastapi_rshb_hakaton/blob/main/src/media/001.jpg" width="600">

## 🚀 Usage
The API returns information for a browser game, implemented on the frontend

👉 A graphical interface is implemented for entering information into the database and loading images.
Used as a graphical interface [SQLAdmin](https://github.com/aminalaee/sqladmin) + [FastAPI Storages](https://github.com/aminalaee/fastapi-storages)

### API method results. Example values | Schema:
Returns a list of game locations with number and name:
`GET /`
```
[
  {
    "number": 0,
    "title": "string",
    "about": "string"
  }
]
```
Returns a list of location dialogues, taking into account the gender of the player:
`GET /dialog/?location_number=<int>&gender=<str>`
```
[
  {
    "number": 0,
    "text": "string"
  }
]
```
Returns a list of location images:
`GET /image/?location_number=<int>`
```
[
  {
    "title": "string",
    "url": "string"
  }
]
```
