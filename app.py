from flask import Flask, request, render_template, jsonify
from flask_cors import cross_origin
import numpy as np

import SFAirbnbPricePrediction as tm

app = Flask(__name__)

@app.route('/get_host_response_time_names', methods=['GET'])
def get_host_response_time_names():
    response = jsonify({
        'host_response_time': tm.get_host_response_time_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_neighbourhood_names', methods=['GET'])
def get_neighbourhood_names():
    response = jsonify({
        'neighbourhood': tm.get_neighbourhood_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_property_type_names', methods=['GET'])
def get_property_type_names():
    response = jsonify({
        'property_type': tm.get_property_type_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_room_type_names', methods=['GET'])
def get_room_type_names():
    response = jsonify({
        'room_type': tm.get_room_type_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/get_cancellation_policy_names', methods=['GET'])
def get_cancellation_policy_names():
    response = jsonify({
        'cancellation_policy': tm.get_cancellation_policy_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_boolean_names', methods=['GET'])
def get_boolean_names():
    response = jsonify({
        'boolean': ["Yes", "No"]
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
# @cross_origin()
def predict():
    if request.method == "POST":
        host_response_rate_pct = float(request.form.get('host_response_rate_pct'))
        host_is_superhost = request.form.get('host_is_superhost')
        host_identity_verified = request.form.get('host_identity_verified')
        accommodates = float(request.form.get('accommodates'))
        bathrooms = float(request.form.get('bathrooms'))
        bedrooms = float(request.form.get('bedrooms'))
        security_deposit = float(request.form.get('security_deposit'))
        cleaning_fee = float(request.form.get('cleaning_fee'))
        guests_included = float(request.form.get('guests_included'))
        extra_people = float(request.form.get('extra_people'))
        min_nights = float(request.form.get('min_nights'))
        max_nights = float(request.form.get('max_nights'))
        number_of_reviews = float(request.form.get('number_of_reviews'))
        instant_bookable = request.form.get('instant_bookable')
        host_listing_count = float(request.form.get('host_listing_count'))
        listing_duration = float(request.form.get('listing_duration'))
        calculated_reviews_per_month = float(request.form.get('calculated_reviews_per_month'))
        review_score = float(request.form.get('review_score'))
        host_is_local = request.form.get('host_is_local')
        host_since_years = float(request.form.get('host_since_years'))
        amenities_count = float(request.form.get('amenities_count'))
        host_response_time = request.form.get('host_response_time')
        neighbourhood = request.form.get('neighbourhood')
        property_type = request.form.get('property_type')
        room_type = request.form.get('room_type')
        cancellation_policy = request.form.get('cancellation_policy')

        prediction = round(float(tm.predict_airbnb_price(host_response_rate_pct, ConvertToBooleanValue(host_is_superhost), \
                    ConvertToBooleanValue(host_identity_verified), accommodates, \
                    bathrooms, bedrooms, np.log1p(security_deposit), np.log1p(cleaning_fee), guests_included, np.log1p(extra_people), \
                    min_nights, max_nights, np.log1p(number_of_reviews), ConvertToBooleanValue(instant_bookable), host_listing_count, listing_duration, \
                    calculated_reviews_per_month, review_score, ConvertToBooleanValue(host_is_local), host_since_years, amenities_count, \
                    host_response_time, neighbourhood, property_type, room_type, cancellation_policy)),2)

        return render_template("index.html", prediction_text="The Airbnb price is $ " + str(prediction))

    return render_template("index.html")


def ConvertToBooleanValue(x):
    if x == "Yes":
        return 1
    else:
        return 0

if __name__ == "__main__":
    tm.load_saved_attributes()
    app.run(debug=True)