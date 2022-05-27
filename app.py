from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@localhost:5432/movie"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

movie_cast = db.Table(
    'movie_cast',
    db.Column('actors_id', db.Integer, db.ForeignKey('actors.id')),
    db.Column('movies_id', db.Integer, db.ForeignKey('movies.id'))
)


class Actors(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    performances = db.relationship('Movies',
                                   secondary=movie_cast,
                                   cascade='all,delete',
                                   backref='movies')

    def __init__(self, name):
        self.name = name


class Directors(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR)
    director_movies = db.relationship('Movies')

    def __init__(self, name):
        self.name = name


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR, nullable=False)
    year = db.Column(db.Integer)
    runtime = db.Column(db.Integer)
    rating = db.Column(db.Numeric)
    gross = db.Column(db.Numeric)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))

    def __init__(self, title, year, runtime, rating, gross):
        self.title = title
        self.year = year
        self.runtime = runtime
        self.rating = rating
        self.gross = gross


@app.route('/movies', methods=['GET'])
def show_movies():
    movies = Movies.query.all()
    results = [
        {
            "id": movie.id,
            "title": movie.title,
            "year": movie.year,
            "runtime": movie.runtime,
            "rating": str(movie.rating),
            "gross": str(movie.gross),
            "director_id": movie.director_id,
        }
        for movie in movies]
    return {"count": len(results), "title": results}


@app.route('/actors', methods=['GET'])
def show_actors():
    actors = Actors.query.all()
    results = [
        {
            "id": actor.id,
            "name": actor.name,
        }
        for actor in actors]
    return {"count": len(results), "actors": results}


@app.route('/actors', methods=['POST'])
def add_actor():
    body = request.get_json()
    db.session.add(Actors(body['name']))
    db.session.commit()
    return 'Actor added to database'


@app.route('/actors/<id>', methods=['PUT'])
def update_actor(id):
    body = request.get_json()
    db.session.query(Actors).filter_by(id=id).update(
        dict(name=body['name']))
    db.session.commit()
    return "Actor updated"


@app.route('/actors/<id>', methods=['DELETE'])
def delete_actor(id):
    actor = db.session.query(Actors).filter(Actors.id == id).first()
    db.session.delete(actor)
    db.session.commit()
    return f"Actor {id} removed from database"


if __name__ == '__main__':
    app.run(debug=True)
