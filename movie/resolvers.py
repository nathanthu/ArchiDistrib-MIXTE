import json

def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

def update_movie_rate(_,info,_id,_rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    # id inconnu : on ne reecrit pas le fichier (sinon il serait vide)
    if not newmovie:
        return None
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

def movie_with_title(_,info,_title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie

def all_movies(_,info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        return json.load(file)['movies']

# renvoie null si l'id existe deja
def add_movie(_,info,_id,_title,_director,_rate):
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
    for movie in movies['movies']:
        if movie['id'] == _id:
            return None
    newmovie = {"id": _id, "title": _title, "director": _director, "rating": _rate}
    movies['movies'].append(newmovie)
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(movies, wfile)
    return newmovie

# renvoie le film supprime, ou null s'il n'existe pas
def delete_movie(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
    for movie in movies['movies']:
        if movie['id'] == _id:
            movies['movies'].remove(movie)
            with open('{}/data/movies.json'.format("."), "w") as wfile:
                json.dump(movies, wfile)
            return movie

def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if movie['id'] in actor['films']]
        return result
