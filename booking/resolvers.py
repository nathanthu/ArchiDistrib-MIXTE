import json
import requests

MOVIE_URL = "http://localhost:3200"
SCHEDULE_URL = "http://localhost:3202"

def read():
    with open('{}/data/bookings.json'.format("."), "r") as file:
        return json.load(file)['bookings']

def write(bookings):
    with open('{}/data/bookings.json'.format("."), "w") as file:
        json.dump({"bookings": bookings}, file)

def all_bookings(_,info):
    return read()

def bookings_by_user(_,info,_userid):
    for booking in read():
        if booking['userid'] == _userid:
            return booking

# renvoie null si le film n'est pas programme ou deja reserve
def add_booking(_,info,_userid,_date,_movieid):
    # REST vers Schedule
    res = requests.get(f"{SCHEDULE_URL}/schedule/{_date}")
    if res.status_code != 200 or _movieid not in res.json()['movies']:
        return None

    bookings = read()
    booking = None
    for b in bookings:
        if b['userid'] == _userid:
            booking = b
    if booking is None:
        booking = {"userid": _userid, "dates": []}
        bookings.append(booking)

    day = None
    for d in booking['dates']:
        if d['date'] == _date:
            day = d
    if day is None:
        day = {"date": _date, "movies": []}
        booking['dates'].append(day)

    if _movieid in day['movies']:
        return None

    day['movies'].append(_movieid)
    write(bookings)
    return booking

# renvoie null si la reservation n'existe pas
def delete_booking(_,info,_userid,_date,_movieid):
    bookings = read()
    for booking in bookings:
        if booking['userid'] == _userid:
            for day in booking['dates']:
                if day['date'] == _date and _movieid in day['movies']:
                    day['movies'].remove(_movieid)
                    if not day['movies']:
                        booking['dates'].remove(day)
                    write(bookings)
                    return booking

# resolver imbrique : ids des films -> films (GraphQL vers Movie)
def resolve_movies_in_date(day, info):
    movies = []
    for movieid in day['movies']:
        query = '{ movie_with_id(_id: "%s") { id title director rating } }' % movieid
        res = requests.post(f"{MOVIE_URL}/graphql", json={'query': query})
        movies.append(res.json()['data']['movie_with_id'])
    return movies
