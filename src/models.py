import os
import sys
from sqlalchemy import  Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    subscription_date = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    
    favorite_planets = relationship("Favorite", back_populates="user", foreign_keys="Favorite.user_id")
    favorite_characters = relationship("Favorite", back_populates="user", foreign_keys="Favorite.user_id")

class Planet(Base):
    __tablename__ = 'planets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    climate = Column(String)
    terrain = Column(String)
    population = Column(Integer)

    characters = relationship("Character", back_populates="homeworld")

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    species = Column(String)
    homeworld_id = Column(Integer, ForeignKey('planets.id'))

    homeworld = relationship("Planet", back_populates="characters")
    
    favorite_by_users = relationship("Favorite", back_populates="character")

class Spaceship(Base):
    __tablename__ = 'spaceships'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    model = Column(String)
    manufacturer = Column(String)
    crew = Column(Integer)
    character_id = Column(Integer, ForeignKey('characters.id'))

    owner = relationship("Character", back_populates="spaceships")

class Favorite(Base):
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    planet_id = Column(Integer, ForeignKey('planets.id'), nullable=True)
    character_id = Column(Integer, ForeignKey('characters.id'), nullable=True)
    
    user = relationship("User", back_populates="favorite_planets", foreign_keys=[user_id])
    character = relationship("Character", back_populates="favorite_by_users", foreign_keys=[character_id])
    planet = relationship("Planet", back_populates="favorite_by_users", foreign_keys=[planet_id])

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
