from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

MOVIE_URL = "http://localhost:3200"
SCHEDULE_URL = "http://localhost:3202"

with open('{}/data/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

def write(bookings):
   with open('{}/data/bookings.json'.format("."), 'w') as f:
      json.dump({"bookings": bookings}, f)

def find_booking(userid):
   for booking in bookings:
      if str(booking["userid"]) == str(userid):
         return booking
   return None

# requete GraphQL vers Movie, renvoie le film ou None
def get_movie(movieid):
   query = '{ movie_with_id(_id: "%s") { id title director rating } }' % movieid
   res = requests.post(f"{MOVIE_URL}/graphql", json={'query': query})
   return res.json()["data"]["movie_with_id"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_bookings():
   return make_response(jsonify(bookings), 200)

@app.route("/bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
   booking = find_booking(userid)
   if booking is None:
      return make_response(jsonify({"error": "no booking for this user"}), 404)
   return make_response(jsonify(booking), 200)

# reservations avec le detail des films (GraphQL vers Movie)
@app.route("/bookings/<userid>/details", methods=['GET'])
def get_user_bookings_details(userid):
   booking = find_booking(userid)
   if booking is None:
      return make_response(jsonify({"error": "no booking for this user"}), 404)

   dates = []
   for day in booking["dates"]:
      movies = [get_movie(movieid) for movieid in day["movies"]]
      dates.append({"date": day["date"], "movies": movies})

   return make_response(jsonify({"userid": userid, "dates": dates}), 200)

# corps : {"date": "...", "movieid": "..."}
@app.route("/bookings/<userid>", methods=['POST'])
def add_booking(userid):
   req = request.get_json()
   date = req["date"]
   movieid = req["movieid"]

   # le film doit etre programme a cette date (REST vers Schedule)
   res = requests.get(f"{SCHEDULE_URL}/schedule/{date}")
   if res.status_code != 200 or movieid not in res.json()["movies"]:
      return make_response(jsonify({"error": "movie not scheduled at this date"}), 400)

   booking = find_booking(userid)
   if booking is None:
      booking = {"userid": userid, "dates": []}
      bookings.append(booking)

   day = None
   for d in booking["dates"]:
      if d["date"] == date:
         day = d
   if day is None:
      day = {"date": date, "movies": []}
      booking["dates"].append(day)

   if movieid in day["movies"]:
      return make_response(jsonify({"error": "booking already exists"}), 409)

   day["movies"].append(movieid)
   write(bookings)
   return make_response(jsonify(booking), 201)

@app.route("/bookings/<userid>/<date>/<movieid>", methods=['DELETE'])
def del_booking(userid, date, movieid):
   booking = find_booking(userid)
   if booking is not None:
      for day in booking["dates"]:
         if day["date"] == date and movieid in day["movies"]:
            day["movies"].remove(movieid)
            if not day["movies"]:
               booking["dates"].remove(day)
            write(bookings)
            return make_response(jsonify(booking), 200)
   return make_response(jsonify({"error": "booking not found"}), 404)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
