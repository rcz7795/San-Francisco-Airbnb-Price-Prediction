import pickle
import json
import numpy as np
from os import path
from xgboost import Booster, XGBRegressor


host_response_time_values = None
neighbourhood_values = None
property_type_values = None
room_type_values = None
cancellation_policy_values = None
model = None

def load_saved_attributes():

    global host_response_time_values
    global neighbourhood_values
    global property_type_values
    global room_type_values
    global cancellation_policy_values
    global model

    with open("columns.json", "r") as f:
        resp = json.load(f)
        host_response_time_values = resp["host_response_time"]
        neighbourhood_values = resp["neighbourhood"]
        property_type_values = resp["property_type"]
        room_type_values = resp["room_type"]
        cancellation_policy_values = resp["cancellation_policy"]

    model = XGBRegressor()
    booster = Booster()
    booster.load_model('airbnb_price_predictor')
    model._Booster = booster

def get_host_response_time_names():
    return host_response_time_values

def get_neighbourhood_names():
    return neighbourhood_values

def get_property_type_names():
    return property_type_values

def get_room_type_names():
    return room_type_values

def get_cancellation_policy_names():
    return cancellation_policy_values

def predict_airbnb_price(host_response_rate_pct, host_is_superhost, host_identity_verified, accommodates, \
                    bathrooms, bedrooms, security_deposit, cleaning_fee, guests_included, extra_people, \
                    min_nights, max_nights, number_of_reviews, instant_bookable, host_listing_count, listing_duration, \
                    calculated_reviews_per_month, review_score, host_is_local, host_since_years, amenities_count, \
                    host_response_time, neighbourhood, property_type, room_type, cancellation_policy):

    try:
        host_response_time_index = host_response_time_values.index(host_response_time)
        neighbourhood_index = neighbourhood_values.index(neighbourhood)
        property_type_index = property_type_values.index(property_type)
        room_type_index = room_type_values.index(room_type)
        cancellation_policy_index = cancellation_policy_values.index(cancellation_policy)

    except:
        host_response_time_index = -1
        neighbourhood_index = -1
        property_type_index = -1
        room_type_index = -1
        cancellation_policy_index = -1

    host_response_time_array = np.zeros(len(host_response_time_values))
    if host_response_time_index >= 0:
        host_response_time_array[host_response_time_index] = 1

    neighbourhood_array = np.zeros(len(neighbourhood_values))
    if neighbourhood_index >= 0:
        neighbourhood_array[neighbourhood_index] = 1

    property_type_array = np.zeros(len(property_type_values))
    if property_type_index >= 0:
        property_type_array[property_type_index] = 1

    room_type_array = np.zeros(len(room_type_values))
    if room_type_index >= 0:
        room_type_array[room_type_index] = 1

    cancellation_policy_array = np.zeros(len(cancellation_policy_values))
    if cancellation_policy_index >= 0:
        cancellation_policy_array[cancellation_policy_index] = 1


    sample = np.concatenate((np.array([host_response_rate_pct, host_is_superhost, host_identity_verified, accommodates, \
                    bathrooms, bedrooms, security_deposit, cleaning_fee, guests_included, extra_people, \
                    min_nights, max_nights, number_of_reviews, instant_bookable, host_listing_count, listing_duration, \
                    calculated_reviews_per_month, review_score, host_is_local, host_since_years, amenities_count]), \
                    host_response_time_array, neighbourhood_array, property_type_array, room_type_array, cancellation_policy_array))

    return model.predict(sample.reshape(1,-1))[0]


if __name__ == '__main__':
    load_saved_attributes()
else:
    load_saved_attributes()
