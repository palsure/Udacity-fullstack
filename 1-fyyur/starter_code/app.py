#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for, 
  abort)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging, sys
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *
from flask_migrate import Migrate
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc@127.0.0.1:5432/fyyurapp'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  count = 10
  venues = Venue.query.order_by(Venue.id.desc(), Venue.created_at.desc()).limit(count).all()
  artists = Artist.query.order_by(Artist.id.desc()).limit(count).all()
  return render_template('pages/home.html', venues=venues, artists=artists)

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  data = []
  # venues = Venue.query.order_by('city', 'state').all()
  # print(venues)
  # for venue in venues:
  #   upcoming_show_count = 0
  #   shows = venue.shows
  #   for show in shows:
  #     if datetime.now() < show.start_time:
  #       upcoming_show_count += 1
  #   venue_group = {}
  #   pointer = -1
  #   if len(data) == 0:
  #     pointer = 0
  #     venue_group = {
  #       "city": venue.city,
  #       "state": venue.state,
  #       "venues": []
  #     }
  #     data.append(venue_group)
  #   else:
  #     for i, d in enumerate(data):
  #       if d['city'] == venue.city and d['state'] == venue.state:
  #         pointer = i
  #         break
  #     if pointer < 0:
  #       venue_group = {
  #         "city": venue.city,
  #         "state": venue.state,
  #         "venues": []
  #       }
  #       data.append(venue_group)
  #       pointer = len(data) - 1
  #     else:
  #       venue_group = data[pointer]
  #   venu_sub_item = {
  #       "id": venue.id,
  #       "name": venue.name,
  #       "num_upcoming_shows": upcoming_show_count
  #     }
  #   venue_group['venues'].append(venu_sub_item)
  #   data[pointer] = venue_group
  venues = Venue.query.all()
  places = Venue.query.distinct(Venue.city, Venue.state).all()
  for place in places:
      data.append({
          'city': place.city,
          'state': place.state,
          'venues': [{
              'id': venue.id,
              'name': venue.name,
              'num_upcoming_shows': len([show for show in venue.shows if show.start_time > datetime.now()])
          } for venue in venues if
              venue.city == place.city and venue.state == place.state]
      })
  
  print(data)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  search_data = request.form.get('search_term', '')
  if search_data.count(",") == 1:
    values = search_data.split(",", 1)
    venues = Venue.query.filter(Venue.city.match(values[0].strip()), Venue.state.match(values[1].strip())).order_by('name').all()
  else:
    # venues = Venue.query.filter(Venue.name.match(search_data)).order_by('name').all()
    venues = Venue.query.filter(Venue.name.ilike("%" + search_data + "%")).order_by('name').all()
  print(venues)
  data = []
  for venue in venues:
    upcoming_show_count = 0
    shows = venue.shows
    for show in shows:
      if datetime.now() < show.start_time:
        upcoming_show_count += 1
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": upcoming_show_count
    })

  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }

  error = False
  venue_data = {}
  try:
    # shows = db.session.query(Show).join(Venue.shows, Artist).filter(Venue.id == venue_id).all()
    # print(len(shows))
    # # venue = Venue.query.filter_by(id=venue_id).first()
    # upcoming_shows_count = 0
    # past_shows_count = 0
    # upcoming_shows = []
    # past_shows = []
    # for show in shows:
    #   show_artist = {
    #         "artist_id": show.artist.id,
    #         "artist_name": show.artist.name,
    #         "artist_image_link": show.artist.image_link,
    #         "start_time": show.start_time
    #     }
    #   if datetime.now() < show.start_time:
    #     upcoming_shows_count += 1
    #     upcoming_shows.append(show_artist)
    #   else:
    #     past_shows_count += 1
    #     past_shows.append(show_artist)
    # if (len(shows) == 0):
    #   venue = Venue.query.filter(Venue.id == venue_id).first()
    # else:
    #   venue = shows[0].venue
    # venue_data = {
    #   "id": venue.id,
    #   "name": venue.name,
    #   "genres": venue.genres,
    #   "address": venue.address,
    #   "city": venue.city,
    #   "state": venue.state,
    #   "phone": venue.phone,
    #   "website": venue.website,
    #   "facebook_link": venue.facebook_link,
    #   "seeking_talent": venue.seeking_talent,
    #   "seeking_description": venue.seeking_description,
    #   "image_link": venue.image_link,
    #   "past_shows": past_shows,
    #   "upcoming_shows": upcoming_shows,
    #   "past_shows_count": past_shows_count,
    #   "upcoming_shows_count": upcoming_shows_count,
    # }
    venue = Venue.query.get_or_404(venue_id)
    past_shows = []
    upcoming_shows = []

    for show in venue.shows:
        temp_show = {
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        }
        if show.start_time <= datetime.now():
            past_shows.append(temp_show)
        else:
            upcoming_shows.append(temp_show)

    # object class to dict
    venue_data = vars(venue)

    venue_data['past_shows'] = past_shows
    venue_data['upcoming_shows'] = upcoming_shows
    venue_data['past_shows_count'] = len(past_shows)
    venue_data['upcoming_shows_count'] = len(upcoming_shows)
    print(venue_data)
  except:
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash("An error occurred. Error in fetching venue details for id: " + str(venue_id))
    abort(500)
  return render_template('pages/show_venue.html', venue=venue_data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form, meta={'csrf': False})
  if form.validate():
    error = False
    seeking_talent = False
    try:
      if request.form['seeking_talent'] == 'y':
        seeking_talent = True
    except:
      print(sys.exc_info())

    try:
      print(request.form)
      venue = Venue(
        name = request.form['name'], 
        city = request.form['city'],
        state = request.form['state'],
        address = request.form['address'],
        phone = request.form['phone'],
        image_link = request.form['image_link'],
        facebook_link = request.form['facebook_link'],
        genres = request.form.getlist('genres'),
        website = request.form['website_link'],
        seeking_description = request.form['seeking_description'],
        seeking_talent = seeking_talent
      )
      db.session.add(venue)
      db.session.commit()
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
    if error:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed!')
      abort(500)
    else:
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    show = db.session.query(Show).filter_by(venue_id=venue_id).first()
    if show:
        db.session.delete(show)
    venue = Venue.query.filter_by(id=venue_id).first()
    # current_session = db.object_session(venue)
    db.session.delete(venue)
    db.session.commit()
    print('delete done')
    flash('Venue ' + venue.name + ' successfully deleted!')
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted!')
    abort(500)
  return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  data = []
  error = False
  try:
    artists = Artist.query.order_by('name').all()
    for artist in artists:
      data.append({
        "id": artist.id,
        "name": artist.name
      })
  except:
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred in fetching artist records')
    abort(500)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  data = []
  error = False
  try:
    search_data = request.form.get('search_term', '')
    if search_data.count(",") == 1:
      values = search_data.split(",", 1)
      artists = Artist.query.filter(Artist.city.match(values[0].strip()), Artist.state.match(values[1].strip())).order_by('name').all()
    else:
      artists = Artist.query.filter(Artist.name.match(search_data)).order_by('name').all()
    print(artists)
    for artist in artists:
      upcoming_show_count = 0
      shows = artist.shows
      for show in shows:
        if datetime.now() < show.start_time:
          upcoming_show_count += 1
      data.append({
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": upcoming_show_count
      })
  except:
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred in searching artist with key - ' + search_data)
    abort(500)
  response = {
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }

  error = False
  artist_data = {}
  try:
    # shows = db.session.query(Show).join(Artist.shows, Venue).filter(Artist.id == artist_id).all()
    # # artist = Artist.query.filter_by(id=artist_id).first()
    # upcoming_shows_count = 0
    # past_shows_count = 0
    # upcoming_shows = []
    # past_shows = []
    # for show in shows:
    #   show_venue = {
    #         "venue_id": show.venue.id,
    #         "venue_name": show.venue.name,
    #         "venue_image_link": show.venue.image_link,
    #         "start_time": show.start_time
    #     }
    #   if datetime.now() < show.start_time:
    #     upcoming_shows_count += 1
    #     upcoming_shows.append(show_venue)
    #   else:
    #     past_shows_count += 1
    #     past_shows.append(show_venue)

    # if (len(shows) == 0):
    #   artist = Artist.query.filter(Artist.id == artist_id).first()
    # else:
    #   artist = shows[0].artist
    # artist_data = {
    #   "id": artist.id,
    #   "name": artist.name,
    #   "genres": artist.genres,
    #   "city": artist.city,
    #   "state": artist.state,
    #   "phone": artist.phone,
    #   "website": artist.website,
    #   "facebook_link": artist.facebook_link,
    #   "seeking_venue": artist.seeking_venue,
    #   "seeking_description": artist.seeking_description,
    #   "image_link": artist.image_link,
    #   "past_shows": past_shows,
    #   "upcoming_shows": upcoming_shows,
    #   "past_shows_count": past_shows_count,
    #   "upcoming_shows_count": upcoming_shows_count,
    # }
    artist = Artist.query.get_or_404(artist_id)
    past_shows = []
    upcoming_shows = []

    for show in artist.shows:
        temp_show = {
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        }
        if show.start_time <= datetime.now():
            past_shows.append(temp_show)
        else:
            upcoming_shows.append(temp_show)

    # object class to dict
    artist_data = vars(artist)
    artist_data['past_shows'] = past_shows
    artist_data['upcoming_shows'] = upcoming_shows
    artist_data['past_shows_count'] = len(past_shows)
    artist_data['upcoming_shows_count'] = len(upcoming_shows)
    print(artist_data)
  except:
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred in fetching artist details for id: ' + str(artist_id))
    abort(500)
  return render_template('pages/show_artist.html', artist = artist_data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.filter_by(id=artist_id).first()
  print(artist)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.genres.data = artist.genres
  form.phone.data = artist.phone
  form.website_link.data = artist.website
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form, meta={"csrf": False})
  if form.validate():
    error = False
    seeking_venue = False
    try:
      if request.form['seeking_venue'] == 'y':
        seeking_venue = True
    except:
      print(sys.exc_info())
    try:
      artist = Artist.query.filter_by(id=artist_id).first()
      print(artist)
      print(request.form)
      artist.name = request.form['name']
      artist.city = request.form['city']
      artist.state = request.form['state']
      artist.phone = request.form['phone']
      artist.image_link = request.form['image_link']
      artist.facebook_link = request.form['facebook_link']
      artist.genres = request.form.getlist('genres')
      artist.website = request.form['website_link']
      artist.seeking_description = request.form['seeking_description']
      artist.seeking_venue = seeking_venue
      db.session.add(artist)
      db.session.commit()
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
    if error:
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated!')
      abort(500)
    else:
      flash('Artist ' + request.form['name'] + ' was successfully updated!')
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
    form = ArtistForm()
    # return render_template('forms/edit_artist.html', form=form)
  
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.filter_by(id=venue_id).first()
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.genres.data = venue.genres
  form.phone.data = venue.phone
  form.website_link.data = venue.website
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form, meta={'csrf': False})
  if form.validate():
    error = False
    seeking_talent = False
    try:
      if request.form['seeking_talent'] == 'y':
        seeking_talent = True
    except:
      print(sys.exc_info())
    try:
      venue = Venue.query.filter_by(id=venue_id).first()
      venue.name = request.form['name']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.address = request.form['address']
      venue.phone = request.form['phone']
      venue.image_link = request.form['image_link']
      venue.facebook_link = request.form['facebook_link']
      venue.genres = request.form.getlist('genres')
      venue.website = request.form['website_link']
      venue.seeking_description = request.form['seeking_description']
      venue.seeking_talent = seeking_talent
      db.session.add(venue)
      db.session.commit()
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
    if error:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated!')
      abort(500)
    else:
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
    form = VenueForm()
  #   return render_template('forms/edit_venue.html', form=form)

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form, meta={'csrf': False})
  if form.validate():
    error = False
    seeking_venue = False
    try:
      if request.form['seeking_venue'] == 'y':
        seeking_venue = True
    except:
      print(sys.exc_info())
    try:
      print(request.form)
      artist = Artist(
        name = request.form['name'], 
        city = request.form['city'],
        state = request.form['state'],
        phone = request.form['phone'],
        image_link = request.form['image_link'],
        facebook_link = request.form['facebook_link'],
        genres = request.form.getlist('genres'),
        website = request.form['website_link'],
        seeking_description = request.form['seeking_description'],
        seeking_venue = seeking_venue
      )
      db.session.add(artist)
      db.session.commit()
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
    if error:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed!')
      abort(500)
    else:
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    message = []
    for field, err in form.errors.items():
        message.append(field + ' ' + '|'.join(err))
    flash('Errors ' + str(message))
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  error = False
  shows_data = []
  try:
    # records = db.session.query(Show, Venue, Artist).join(Venue, Show.venue_id == Venue.id).join(Artist, Show.artist_id == Artist.id).order_by(Show.start_time.desc()).all();
    shows = Show.query.all()
    for show in shows:
      shows_data.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      })
    print(shows_data)
  except:
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred in fetching shows')
    abort(500)
  return render_template('pages/shows.html', shows=shows_data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  form = ShowForm(request.form, meta={"csrf": False})
  if form.validate():
    try:
      print(request.form)
      show = Show(
        artist_id = request.form['artist_id'], 
        venue_id = request.form['venue_id'],
        start_time = request.form.get('start_time', '')
      )
      db.session.add(show)
      db.session.commit()
    except:
      db.session.rollback()
      error = True
      print(sys.exc_info())
    finally:
      db.session.close()
    if error:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      flash('An error occurred. Show could not be listed!')
      abort(500)
    else:
      # on successful db insert, flash success
      flash('Show was successfully listed!')
  else:
    for field, message in form.errors.items():
      flash(field + ' - ' + str(message), 'danger')
  return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
