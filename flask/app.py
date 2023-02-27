from flask import Flask, request, jsonify, abort
from sqlalchemy import create_engine, select, asc, desc, inspect, func, distinct
from sqlalchemy.orm import sessionmaker, Session, joinedload

from models import Author, Title, Publisher, Book, Base
from matmodels import Dist_books_authors, Sum_books_authors, T_stat, Ta_stat, Avg_pub_to_lib_stat, Avg_age, Min_age, Max_age, Younger_than_avg
from utils import is_valid, schemas, get_books
from mat_refresh import mat

from dateutil import parser
import re

import datetime

db = create_engine("postgresql+psycopg://postgres:valami@postgres/library", echo=True)
Session = sessionmaker(db)

app = Flask(__name__)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(418)  # ez mindenkepp kell :D
def im_a_teapot(e):
    return jsonify(error=str(e)), 418


@app.route("/getall0/p/<int:page_number>/<int:limit>", methods=['GET'])
def getall0(page_number, limit):

    if page_number < 1:
        abort(400, description='page number must >= 1')
    else:
        offset = (page_number - 1) * limit

        with Session() as session:
            result = session.scalars(
                select(Book).order_by(asc('id')).limit(limit).offset(offset)
            )
            return get_books.results(result)  # return a sessionon belul van


@app.route("/getall/p/<int:page_number>/<int:limit>", methods=['GET'])
def getall(page_number, limit):

    if page_number < 1:
        abort(400, description='page number must >= 1')
    else:
        offset = (page_number - 1) * limit

    with Session() as session:
        result = session.scalars(
            select(Book)
            .options(joinedload(Book.author))
            .options(joinedload(Book.publisher))
            .options(joinedload(Book.title))
            .order_by(asc('id')).limit(limit).offset(offset), execution_options={"prebuffer_rows": True}
        )

    return get_books.results(result)  # return a sessionon kivul van + prebuffer + joinedload


@app.route("/search/author/<author>", methods=['GET'])
def searchAuthor(author):

    with Session() as session:
        if len(author) < 3:
            abort(400, description='At least 3 characters please')
        else:
            result = session.scalars(
                select(Book).join(Author).filter(Author.flname.like('%'+author+'%')).order_by(asc('id')).limit(100)
            )
            return get_books.results(result)


@app.route("/search/title/<title>", methods=['GET'])
def searchTitle(title):

    with Session() as session:
        if len(title) < 3:
            abort(400, description='At least 3 characters please')
        else:
            result = session.scalars(
                select(Book).join(Title).filter(Title.title.like('%'+title+'%')).order_by(asc('id')).limit(100)
            )
            return get_books.results(result)


@app.route("/search/publisher/<publisher>", methods=['GET'])
def searchPublisher(publisher):

    with Session() as session:
        if len(publisher) < 3:
            abort(400, description='At least 3 characters please')
        else:
            result = session.scalars(
                select(Book).join(Publisher).filter(Publisher.publisher.like('%'+publisher+'%')).order_by(asc('id')).limit(100)
            )
            return get_books.results(result)


@app.route("/add", methods=['POST'])
def add():

    if request.is_json == False:
        abort(400, description='Its not a JSON')
    else:
        data = request.json
    if is_valid.json(schemas.book_schema, data) == False:
        abort(400, description='Its not a valid JSON')
    else:
        flname = data.get('flname')
        lib_date = data.get('lib_date')
        pub_date = data.get('pub_date')
        publisher = data.get('publisher')
        title = data.get('title')
    try:
        if bool(re.match('^\d{4}-\d{2}-\d{2}$', pub_date)) == False or bool(parser.parse(pub_date)) != True:
            raise
    except:
        abort(400, description='pub_date - wrong date format')
    try:
        if bool(re.match('^\d{4}-\d{2}-\d{2}$', lib_date)) == False or bool(parser.parse(lib_date)) != True:
            raise
    except:
        abort(400, description='lib_date - wrong date format')
    if len(flname) == 0:
        abort(400, description='flname - field has 0 length')
    elif len(publisher) == 0:
        abort(400, description='publisher - field has 0 length')
    elif len(title) == 0:
        abort(400, description='title - field has 0 length')
    else:
        with Session() as session:

            author_obj = session.scalars(select(Author).filter(Author.flname == flname)).first()
            if author_obj == None:
                author_obj = Author(flname=flname)

            title_obj = session.scalars(
                select(Title).filter(Title.title == title)).first()
            if title_obj == None:
                title_obj = Title(title=title)

            publisher_obj = session.scalars(select(Publisher).filter(Publisher.publisher == publisher)).first()
            if publisher_obj == None:
                publisher_obj = Publisher(publisher=publisher)

            book = Book(author=author_obj, title=title_obj, publisher=publisher_obj, pub_date=pub_date, lib_date=lib_date)

            session.add(book)
            session.commit()
            session.refresh(book)

            mat.refresh()
            return jsonify({'last inserted id': book.id})


# egy szerzonek hany egyedi konyve van a DBben
@app.route("/dist_books_authors", methods=['GET'])
def dist_books_authors():

    with Session() as session:
        result = session.scalars(
            select(Dist_books_authors).order_by(desc('count')), execution_options={"prebuffer_rows": True}
        )

    book = []
    for i in result:
        mydict = {
            'id': i.id,
            'author': i.flname,
            'count': i.count,
        }
        book.append(mydict)

    return (jsonify(book))


# egy szerzonek osszesen hany konyve van a DBben
@app.route("/sum_books_authors", methods=['GET'])
def sum_books_authors():

    with Session() as session:
        result = session.scalars(
            select(Sum_books_authors).order_by(desc('count')), execution_options={"prebuffer_rows": True}
        )

    book = []
    for i in result:
        mydict = {
            'id': i.id,
            'author': i.flname,
            'count': i.count,
        }
        book.append(mydict)

    return (jsonify(book))


# azonos cimu konyvbol hany peldany van (kulonbozo szerzonek lehetnek azonos cimu konyvei)
@app.route("/t_stat", methods=['GET'])
def t_stat():

    with Session() as session:
        result = session.scalars(
            select(T_stat).order_by(desc('count')), execution_options={"prebuffer_rows": True}
        )

    book = []
    for i in result:
        mydict = {
            'id': i.id,
            'title': i.title,
            'count': i.count,
        }
        book.append(mydict)

    return (jsonify(book))


# azonos cimu konyvbol hany peldany van (kulonbozo szerzok azonos cimu konyvei nem szamitanak)
@app.route("/ta_stat", methods=['GET'])
def ta_stat():

    with Session() as session:
        result = session.scalars(
            select(Ta_stat).order_by(desc('count')), execution_options={"prebuffer_rows": True}
        )

    book = []
    for i in result:
        mydict = {
            'title_id': i.title_id,
            'author_id': i.author_id,
            'title': i.title,
            'flnamer': i.flname,
            'count': i.count,
        }
        book.append(mydict)

    return (jsonify(book))


# megjelenestol a konyvtarba kerulesig eltelt ido atlaga szerzonkent
@app.route("/avg_pub_to_lib_stat", methods=['GET'])
def avg_pub_to_lib_stat():

    with Session() as session:
        result = session.scalars(
            select(Avg_pub_to_lib_stat).order_by(desc('avg_day')), execution_options={"prebuffer_rows": True}
        )

    book = []
    for i in result:
        mydict = {
            'author_id': i.author_id,
            'flname': i.flname,
            'count': i.count,
            'avg_day': i.avg_day
        }
        book.append(mydict)
    return (jsonify(book))


# atlagos eletkora a konyveknek
@app.route("/avg_age", methods=['GET'])
def avg_age():

    with Session() as session:
        result = session.scalars(
            select(Avg_age)
        )

        book = []
        for i in result:
            mydict = {
                'avg': ('{:.2f}'.format(i.avg.days/365))
            }
            book.append(mydict)
        return (jsonify(book))


# legfiatalabb konyv
@app.route("/min_age", methods=['GET'])
def min_age():

    with Session() as session:
        result = session.scalars(
            select(Min_age)
        )

        book = []
        for i in result:
            mydict = {
                'min': ('{:.2f}'.format(i.min.days/365))
            }
            book.append(mydict)
        return (jsonify(book))


# legidosebb konyv
@app.route("/max_age", methods=['GET'])
def max_age():

    with Session() as session:
        result = session.scalars(
            select(Max_age)
        )

        book = []
        for i in result:
            mydict = {
                'max': ('{:.2f}'.format(i.max.days/365))
            }
            book.append(mydict)
        return (jsonify(book))


# atlagnal fiatalabb konyvek
@app.route("/younger_than_avg", methods=['GET'])
def younger_than_avg():

    with Session() as session:
        result = session.scalars(
            select(Younger_than_avg).order_by(desc('age')), execution_options={"prebuffer_rows": True}
        )

    book = []
    for i in result:
        mydict = {
            'id': i.id,
            'flname': i.flname,
            'title': i.title,
            'age': ('{:.2f}'.format(i.age.days/365))
        }
        book.append(mydict)
    return (jsonify(book))


if __name__ == "__main__":
    app.run(debug=True)
