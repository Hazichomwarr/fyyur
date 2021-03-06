#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from email.policy import default
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
# (this part taken care of in the config file)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String(120))
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(500))
    shows = db.relationship('Show', backref=db.backref('venue'), lazy="joined", cascade='all, delete')
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(500))
    shows = db.relationship('Show', backref=db.backref('artist'), lazy="joined", cascade='all, delete')
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'shows'

    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), primary_key=True)
    start_time = db.Column(db.DateTime(), default=datetime.now())
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
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  datas = db.session.query(Venue).all()
  return render_template('pages/venues.html', venues=datas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term', '')
  response = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

  return render_template('pages/search_venues.html', results=response, search_term=search_term, count=len(response))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Venue.query.get_or_404(venue_id)
  upcoming = db.session.query(Show).filter(Show.venue_id==venue_id,Show.start_time>datetime.now()).all()
  past = db.session.query(Show).filter(Show.venue_id==venue_id,Show.start_time<datetime.now()).all()

  return render_template('pages/show_venue.html', venue=data,
  upcoming_shows=upcoming, count_upcoming=len(upcoming),past_shows=past, count_past=len(past))

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
  form = VenueForm()

  new_venue = Venue(
    name=form.name.data, 
    city=form.city.data, 
    state=form.state.data, 
    address=form.address.data, 
    phone=form.phone.data, 
    genres=form.genres.data, 
    facebook_link=form.facebook_link.data,
    image_link=form.image_link.data,
    website_link=form.website_link.data,
    seeking_talent=form.seeking_talent.data,
    description=form.seeking_description.data
    )
  
  # on successful db insert, flash success
  try:
    db.session.add(new_venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except:
    flash('An error occurred. Venue ' + new_venue.name + ' could not be listed.')
  
  finally:
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_term=request.form.get('search_term', '')
  response = Artist.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  return render_template('pages/search_artists.html', results=response, search_term=search_term, count=len(response))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  data = Artist.query.get_or_404(artist_id)
 
  upcoming_shows = db.session.query(Show).filter(Show.artist_id==artist_id,Show.start_time>datetime.now()).all()
  past_shows = db.session.query(Show).filter(Show.artist_id==artist_id,Show.start_time<datetime.now()).all()
  # import pdb
  # pdb.set_trace()
  return render_template('pages/show_artist.html', artist=data, 
  upcoming_shows=upcoming_shows, past_shows=past_shows, count_upcoming=len(upcoming_shows), 
  count_past_shows=len(past_shows)
  )

  
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get_or_404(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm()

  artist.id = artist.id
  artist.name=form.name.data
  artist.city=form.city.data
  artist.state=form.state.data 
  artist.phone=form.phone.data,
  artist.genres=form.genres.data
  artist.facebook_link=form.facebook_link.data
  artist.image_link=form.image_link.data
  artist.website_link=form.website_link.data
  artist.seeking_venue=form.seeking_venue.data
  artist.description=form.seeking_description.data

  try:
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    return redirect(url_for('show_artist', artist_id=artist.id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  # TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.get_or_404(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  venue = Venue.query.get_or_404(venue_id)

  if not form.name.data in ['', ' ', '  ','   ']:
    venue.name = form.name.data
  if not form.city.data in ['', ' ', '  ','   ']:
    venue.city = form.city.data
  if not form.state.data in ['', ' ', '  ','   ']:
    venue.state = form.state.data
  if not form.address.data in ['', ' ', '  ','   ']:
    venue.address = form.address.data
  if not form.phone.data in ['', ' ', '  ','   ']:
    venue.phone = form.phone.data
  if not form.image_link.data in ['', ' ', '  ','   ']:
    venue.image_link = form.image_link.data
  if not form.facebook_link.data in ['', ' ', '   ','   ']:
    venue.facebook_link = form.facebook_link.data
  if not form.genres.data in ['', ' ', '  ','   ']:
    venue.genres = form.genres.data
  if not form.website_link.data in ['', ' ', '  ','   ']:
    venue.website_link = form.website_link.data
  if form.seeking_talent.data:
    venue.seeking_talent = form.seeking_talent.data
  if not form.seeking_description.data in ['', ' ', '  ','   ']:
    venue.description = form.seeking_description.data
  
  try:
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    return redirect(url_for('show_venue', venue_id=venue.id))

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
  form = ArtistForm()

  new_artist = Artist(
    name=form.name.data, 
    city=form.city.data, 
    state=form.state.data, 
    phone=form.phone.data, 
    genres=form.genres.data, 
    facebook_link=form.facebook_link.data,
    image_link=form.image_link.data,
    website_link=form.website_link.data,
    seeking_venue=form.seeking_venue.data,
    description=form.seeking_description.data
    )

  # on successful db insert, flash success
  try:
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')


  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
  finally:
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = Show.query.all()

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  form = ShowForm()
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  new_show = Show(artist_id=form.artist_id.data, venue_id=form.venue_id.data, start_time=form.start_time.data)
  
  # on successful db insert, flash success
  try:
    db.session.add(new_show)
    db.session.commit()
    flash('Show was successfully listed!')

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except:
    flash('An error occurred. Show could not be listed.')
  finally:
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
