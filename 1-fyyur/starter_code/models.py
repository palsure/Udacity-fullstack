#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from datetime import datetime
from flask_migrate import Migrate
from flask_moment import Moment

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
  # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website = db.Column(db.String(500), nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=True, default=False)
    shows = db.relationship('Show', backref='venue', lazy='joined', cascade="all, delete")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
      return f'<Venue: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, address: {self.address}, phone: {self.phone}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, genres: {self.genres}, website: {self.website}, seeking_description: {self.seeking_description}, seeking_talent: {self.seeking_talent}, shows: {self.shows}>'
    
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
  # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(500), nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=True, default=False)
    shows = db.relationship('Show', backref='artist', lazy='joined', cascade="all, delete")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def __repr__(self):
      return f'<Artist: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}, phone: {self.phone}, genres: {self.genres}, image_link: {self.image_link}, facebook_link: {self.facebook_link}, website: {self.website}, seeking_description: {self.seeking_description}, seeking_venue: {self.seeking_venue}, shows: {self.shows}>'
    
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
      return f'<Show: {self.id}, artist_id: {self.artist_id}, venue_id: {self.venue_id}, start_time: {self.start_time}>'
