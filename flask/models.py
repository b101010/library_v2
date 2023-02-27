from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, text, func
from typing import List
import datetime


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    flname: Mapped[str] = mapped_column(String(400), unique=True)
    book: Mapped[List["Book"]] = relationship(back_populates="author")


class Title(Base):
    __tablename__ = "titles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250), unique=True)
    book: Mapped[List["Book"]] = relationship(back_populates="title")


class Publisher(Base):
    __tablename__ = "publishers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    publisher: Mapped[str] = mapped_column(String(250), unique=True)
    book: Mapped[List["Book"]] = relationship(back_populates="publisher")


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title_id: Mapped[int] = mapped_column(ForeignKey("titles.id", ondelete="CASCADE"))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id", ondelete="CASCADE"))
    pub_date: Mapped[datetime.date] = mapped_column()
    lib_date: Mapped[datetime.date] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    title: Mapped["Title"] = relationship(back_populates="book")
    author: Mapped["Author"] = relationship(back_populates="book")
    publisher: Mapped["Publisher"] = relationship(back_populates="book")