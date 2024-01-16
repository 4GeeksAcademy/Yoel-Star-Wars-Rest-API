from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column
from sqlalchemy import Table
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import String, Integer, Float, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from flask import Flask


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('planet_id', Integer, ForeignKey('planet.id'), nullable=True, primary_key=True),
    Column('character_id', Integer, ForeignKey('character.id'), nullable=True, primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str]  = mapped_column(unique=True)
    name: Mapped[str]
    last_name: Mapped[Optional[str]] = mapped_column()
    email: Mapped[str] 
    country: Mapped[Optional[str]] = mapped_column()
    planets: Mapped[List["Planet"]] = relationship(secondary=association_table)
    characters: Mapped[List["Character"]] = relationship(secondary=association_table)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] 
    population: Mapped[int] = mapped_column(nullable=True)
    gravity: Mapped[int] = mapped_column(nullable=True)
    climate: Mapped[str] = mapped_column(nullable=True)
    users: Mapped[List["User"]] = relationship(secondary=association_table)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "gravity": self.gravity,
            "climate": self.climate,
        }
   
class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] 
    last_name: Mapped[str] = mapped_column(nullable=True)
    eye_color: Mapped[str] = mapped_column(nullable=True)
    height: Mapped[int] = mapped_column(nullable=True)
    origin_planet: Mapped[str] = mapped_column(nullable=True)
    users: Mapped[List["User"]] = relationship(secondary=association_table)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "eye_color": self.eye_color,
            "origin_planet": self.origin_planet
        }
