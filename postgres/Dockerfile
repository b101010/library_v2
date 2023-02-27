FROM postgres:14.7

ENV LANG=C.UTF-8

ENV POSTGRES_PASSWORD=valami

COPY ./0plibrary.sql /docker-entrypoint-initdb.d/
COPY ./1mview.sql /docker-entrypoint-initdb.d/