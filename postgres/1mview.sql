\connect library

CREATE MATERIALIZED VIEW dist_books_authors AS
SELECT authors.id, authors.flname, count(DISTINCT books.title_id) AS count 
FROM books JOIN authors ON authors.id = books.author_id GROUP BY authors.id, authors.flname;

CREATE UNIQUE INDEX ON public.dist_books_authors (id);


CREATE MATERIALIZED VIEW sum_books_authors AS
SELECT authors.id, authors.flname, count(books.title_id) AS count 
FROM books JOIN authors ON authors.id = books.author_id GROUP BY authors.id, authors.flname;

CREATE UNIQUE INDEX ON public.sum_books_authors (id);


CREATE MATERIALIZED VIEW t_stat AS
SELECT titles.id, titles.title, count(books.title_id) AS count 
FROM books JOIN titles ON titles.id = books.title_id GROUP BY titles.id, titles.title;

CREATE UNIQUE INDEX ON public.t_stat (id);


CREATE MATERIALIZED VIEW ta_stat AS
SELECT titles.title, titles.id as title_id, authors.flname, authors.id as author_id, count(books.title_id) AS count,
row_number() over (order by count(books.title_id) desc) id
FROM books JOIN titles ON titles.id = books.title_id JOIN authors ON authors.id = books.author_id 
GROUP BY titles.title, titles.id, authors.flname, authors.id;

CREATE UNIQUE INDEX ON public.ta_stat (id);


CREATE MATERIALIZED VIEW avg_pub_to_lib_stat AS
SELECT authors.id as author_id, authors.flname, count(books.title_id), avg(books.lib_date - books.pub_date)::INTEGER AS avg_day
FROM books JOIN authors ON authors.id = books.author_id GROUP BY authors.id, authors.flname;

CREATE UNIQUE INDEX ON public.avg_pub_to_lib_stat (author_id);


CREATE MATERIALIZED VIEW avg_age AS
SELECT avg(age(now(),pub_date)) FROM books;

CREATE UNIQUE INDEX ON public.avg_age (avg);


CREATE MATERIALIZED VIEW min_age AS
SELECT min(age(now(),pub_date)) FROM books;

CREATE UNIQUE INDEX ON public.min_age (min);


CREATE MATERIALIZED VIEW max_age AS
SELECT max(age(now(),pub_date)) FROM books;

CREATE UNIQUE INDEX ON public.max_age (max);


CREATE MATERIALIZED VIEW younger_than_avg AS
SELECT books.id, authors.flname, titles.title, age(now(),pub_date) AS age 
FROM books LEFT JOIN authors ON books.author_id = authors.id LEFT JOIN titles ON books.title_id = titles.id 
WHERE age(now(),pub_date) < (SELECT avg(age(now(),pub_date)) FROM books);

CREATE UNIQUE INDEX ON public.younger_than_avg (id);