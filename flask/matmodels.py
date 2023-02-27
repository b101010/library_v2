from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, text, func
from typing import List
import datetime


class Base(DeclarativeBase):
    pass


class Dist_books_authors(Base):
    __tablename__ = "dist_books_authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    flname: Mapped[str] = mapped_column(String(400), unique=True)
    count: Mapped[int] = mapped_column(Integer())


class Sum_books_authors(Base):
    __tablename__ = "sum_books_authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    flname: Mapped[str] = mapped_column(String(400), unique=True)
    count: Mapped[int] = mapped_column(Integer())


class T_stat(Base):
    __tablename__ = "t_stat"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True)
    count: Mapped[int] = mapped_column(Integer())


class Ta_stat(Base):
    __tablename__ = "ta_stat"
    title_id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True)
    flname: Mapped[str] = mapped_column(String(400), unique=True)
    count: Mapped[int] = mapped_column(Integer())


class Avg_pub_to_lib_stat(Base):
    __tablename__ = "avg_pub_to_lib_stat"
    author_id: Mapped[int] = mapped_column(primary_key=True)
    flname: Mapped[str] = mapped_column(String(400), unique=True)
    count: Mapped[int] = mapped_column(Integer())
    avg_day: Mapped[int] = mapped_column(Integer())


class Avg_age(Base):
    __tablename__ = "avg_age"
    avg: Mapped[datetime.timedelta] = mapped_column(String(50), primary_key=True)


class Min_age(Base):
    __tablename__ = "min_age"
    min: Mapped[datetime.timedelta] = mapped_column(String(50), primary_key=True)


class Max_age(Base):
    __tablename__ = "max_age"
    max: Mapped[datetime.timedelta] = mapped_column(String(50), primary_key=True)


class Younger_than_avg(Base):
    __tablename__ = "younger_than_avg"
    id: Mapped[int] = mapped_column(primary_key=True)
    flname: Mapped[str] = mapped_column(String(400))
    title: Mapped[str] = mapped_column(String(250))
    age: Mapped[datetime.timedelta] = mapped_column(String(50))