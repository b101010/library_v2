# Library backend v2

Nginx\
PostgreSQL\
Flask\
SQLAlchemy

## Nginx

```docker
FROM nginx:1.23

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/
```
```
server {
    listen 80;
    server_name IP_ADDRESS;

    location / {
        #include /etc/nginx/proxy_params;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://flask:5000;
    }
}
```
## Flask + Gunicorn
```docker
FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--reload", "app:app"]
```

## PostgreSQL
```docker
FROM postgres:14.7

ENV LANG=C.UTF-8

ENV POSTGRES_PASSWORD=valami

COPY ./0plibrary.sql /docker-entrypoint-initdb.d/
COPY ./1mview.sql /docker-entrypoint-initdb.d/
```
itt hozom létre a DB-t és a Materialized Vieweket

## Docker-compose
A 3 containert a docker-compose segítségével buildelem, és indítom el.
```shell
docker-compose build
docker-compose up
```

```yaml
version: "3.7"

services:

  flask:
    build: ./flask
    container_name: flask
    restart: always
    expose:
      - 5000
    networks:
      - my-network

  nginx:
    build: ./nginx
    container_name: nginx
    restart: always
    ports:
      - 80:80
    networks:
      - my-network
    depends_on:
      - flask

  postgres:
    build: ./postgres
    container_name: postgres
    restart: always
    expose:
      - 5432
    # ports:
    #   - 5432:5432
    networks:
      - my-network
    depends_on:
      - flask
    
networks:
  my-network:
```

## Minden lekérdezés egy JSON-t ad vissza.
### Összes könyv lekérdezése

```
/getall0/p/<int:page_number>/<int:limit>
/getall/p/<int:page_number>/<int:limit>
```
A resultok pagekre bontva kérdezhetőek le  
pl.: .../getall/p/3/100

**getall** prebuffer + joinedload  
**getall0** nincs se prebuffer, se joinedload  
Direkt hagytam itt mindkettőt, hogy össze lehessen hasonlítani.

### Keresés szerzőkre, címekre, kiadókra
```
/search/author/<author>
/search/title/<title>
/search/publisher/<publisher>
```
A keresés case és accent sensitive, minimum 3 karaktert kell megadni.

### Új könyv hozzáadása
```
/add
```
Postolni kell egy megfelelő JSONt.
```
{
    "flname": "Károly Simonyi",
    "lib_date": "2011-04-17",
    "pub_date": "2012-02-21",
    "publisher": "Akadémiai kiadó",
    "title": "A fizika kultúrtörténete"
}
```
A POST után egy sor ellenőrzés következik:
- valóban JSON van a postban
- a JSONban a megfelelő mezők vannak
- a dátumoknak '^\d{4}-\d{2}-\d{2}$' formátumban kell lenniük
- értelmes dátumot kell megadni
- egyik mezőnek sem lehet 0 a hossza

Miután bekerültek az adatok a DBbe frissülnek a Materialized View-ek, de ez elég lassan történik meg ~580ms... :( Lehet, hogy érdemesebb lenne CRONból futtatni.

## Statisztikák

A statisztikák Materialized Viewekben vannak tárolva

Egy szerzőnek hány egyedi könyve van a DBben  
```
/dist_books_authors
```
Egy szerzőnek összesen hány könyve van a DBben  
```
/sum_books_authors
```

Azonos címu könyvből hány példany van (különböző szerzőnek lehetnek azonos című könyvei)  
```
/t_stat
```

Azonos című könyvből hány példány van (különböző szerzők azonos cimű könyvei nem számítanak)
```
/ta_stat
```

Megjelenéstől a könyvtásba kerülésig eltelt idő (év) átlaga szerzőnként
```
/avg_pub_to_lib_stat
```

Átlagos életkora (év) a könyveknek
```
/avg_age
```

Legfiatalabb könyv kora
```
/min_age
```

Legidősebb könyv kora
```
/max_age
```

Átlagnál fiatalabb könyvek
```
/younger_than_avg
```


