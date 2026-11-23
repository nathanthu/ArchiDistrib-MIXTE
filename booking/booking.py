from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response

import resolvers as r

PORT = 3201
HOST = '0.0.0.0'
app = Flask(__name__)

type_defs = load_schema_from_path('booking.graphql')
query = QueryType()
mutation = MutationType()
booking = ObjectType('Booking')
bookingdate = ObjectType('BookingDate')
movie = ObjectType('Movie')

query.set_field('all_bookings', r.all_bookings)
query.set_field('bookings_by_user', r.bookings_by_user)
mutation.set_field('add_booking', r.add_booking)
mutation.set_field('delete_booking', r.delete_booking)
bookingdate.set_field('movies', r.resolve_movies_in_date)

schema = make_executable_schema(type_defs, query, mutation, booking, bookingdate, movie)

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Booking service!</h1>",200)

# graphql entry points
@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
                        schema,
                        data,
                        context_value=None,
                        debug=app.debug
                    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
