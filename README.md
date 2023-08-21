## 🎂 EpicCakes

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat&logo=gunicorn&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue?style=flat&logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat&logo=nginx&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

АPI for online store

<img src="https://github.com/StefanEpic/fastapi_epiccakes/blob/main/src/media/001.jpg" width="600">

## 🍰 Usage
The API allows you to work with online store requests. Allows you to work with entities: products, orders, manufacturers, customers, reviews. There is also registration and authorization, admin panel.

## 🍪 API demo
You can test:

[Docs](http://31.129.98.245/docs):

- username: admin@admin.com
- password: 12345

[Admin panel](http://31.129.98.245/admin):

- username: admin@admin.com
- password: 12345

## 🍩 Tests
```
Name                                    Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------------------
src/__init__.py                             0      0      0      0   100%
src/api/__init__.py                         0      0      0      0   100%
src/api/auth/__init__.py                    0      0      0      0   100%
src/api/auth/auth.py                       13      0      0      0   100%
src/api/auth/user.py                       31      1      0      0    97%
src/api/routers.py                         13      0      0      0   100%
src/api/sqladmin/__init__.py                0      0      0      0   100%
src/api/sqladmin/views.py                  38      5      4      1    81%
src/api/store/__init__.py                   0      0      0      0   100%
src/api/store/category.py                  27      0      0      0   100%
src/api/store/customer.py                  27      0      0      0   100%
src/api/store/customer_manager.py          32      0      2      0   100%
src/api/store/image.py                     26      0      0      0   100%
src/api/store/manufacturer.py              27      0      0      0   100%
src/api/store/manufacturer_manager.py      32      0      2      0   100%
src/api/store/order.py                     37      0      4      0   100%
src/api/store/product.py                   32      0      2      0   100%
src/api/store/review.py                    32      0      0      0   100%
src/api/store/staff_manager.py             24      0      0      0   100%
src/db/__init__.py                          0      0      0      0   100%
src/db/db.py                               19      3      2      0    76%
src/main.py                                21      2      4      0    92%
src/models/__init__.py                      0      0      0      0   100%
src/models/auth.py                         59      2      6      0    97%
src/models/store.py                       341     10      6      3    96%
src/repositories/__init__.py                0      0      0      0   100%
src/repositories/store.py                 126      0     20      0   100%
src/repositories/user.py                   31      0      2      0   100%
src/utils/__init__.py                       0      0      0      0   100%
src/utils/auth.py                          69      4     12      4    90%
src/utils/repository.py                    49      1      4      0    98%
src/utils/validators.py                    18      0      8      0   100%
src/views/__init__.py                       0      0      0      0   100%
src/views/sqladmin.py                      64      0      0      0   100%
-------------------------------------------------------------------------
TOTAL                                    1188     28     78      8    97%
```
