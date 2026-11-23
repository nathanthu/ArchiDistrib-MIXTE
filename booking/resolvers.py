import requests
from pymongo import MongoClient

MOVIE_URL = "http://movie:3200"
SCHEDULE_URL = "http://schedule:3202"

# collection "bookings" de la base "booking"
bookings = MongoClient("mongodb://mongo:27017")["booking"]["bookings"]

def all_bookings(_,info):
    return list(bookings.find())

def bookings_by_user(_,info,_userid):
    return bookings.find_one({"userid": _userid})

# renvoie null si le film n'est pas programme ou deja reserve
def add_booking(_,info,_userid,_date,_movieid):
    # REST vers Schedule
    res = requests.get(f"{SCHEDULE_URL}/schedule/{_date}")
    if res.status_code != 200 or _movieid not in res.json()['movies']:
        return None

    booking = bookings.find_one({"userid": _userid})
    if booking is None:
        booking = {"userid": _userid, "dates": []}

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
    # upsert : cree le document s'il n'existe pas
    bookings.replace_one({"userid": _userid}, booking, upsert=True)
    return booking

# renvoie null si la reservation n'existe pas
def delete_booking(_,info,_userid,_date,_movieid):
    booking = bookings.find_one({"userid": _userid})
    if booking is None:
        return None
    for day in booking['dates']:
        if day['date'] == _date and _movieid in day['movies']:
            day['movies'].remove(_movieid)
            if not day['movies']:
                booking['dates'].remove(day)
            bookings.replace_one({"userid": _userid}, booking)
            return booking

# resolver imbrique : ids des films -> films (GraphQL vers Movie)
def resolve_movies_in_date(day, info):
    movies = []
    for movieid in day['movies']:
        query = '{ movie_with_id(_id: "%s") { id title director rating } }' % movieid
        res = requests.post(f"{MOVIE_URL}/graphql", json={'query': query})
        movies.append(res.json()['data']['movie_with_id'])
    return movies
