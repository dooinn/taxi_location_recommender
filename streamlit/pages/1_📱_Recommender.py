import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import requests
from geopy.distance import geodesic
import pickle
import numpy as np
from datetime import datetime
import pytz  # For timezone handling




# Load the model and data
with open('kmeans_model.pkl', 'rb') as file:
    loaded_kmeans = pickle.load(file)
with open('nearest_neighbors_model.pkl', 'rb') as file:
    loaded_nearest_neighbors = pickle.load(file)

cluster_centers = pd.read_csv('cluster_centers.csv')
trips = pd.read_csv('/Users/dooinnkim/jupyter_notebook/ironhacks/taxi_location_recommender/datasets/trips_clusters_sample.csv') 





def get_location_details(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        location_name = data.get('display_name')
        return location_name
    else:
        return "Location details not available"
    
    
def calculate_citywide_average_distance(current_location, cluster_centers):
    all_distances = cluster_centers.apply(lambda row: geodesic(current_location, (row['pickup_latitude'], row['pickup_longitude'])).kilometers, axis=1)
    return all_distances.mean()

def recommend_pickup_locations(current_location, current_time, current_date, model, cluster_data, historical_data):
    """
    1. Calculates the city-wide average distance to all hotspots from the user's current location.
    2. Calculates distance scores for each recommended location based on how their distance compares to the city-wide average.
    3. Calculates popularity scores based on the relative 'busyness' (here represented by the 'count' of trips) of each recommended location compared to the most popular location.
    4. Combines these scores into a final 'recommendation_score' for each recommended location.
    5. Sorts recommended locations by this combined score before returning them.
    """
    
    
    avg_distance_all_hotspots = calculate_citywide_average_distance(current_location, cluster_data)
    
    current_time = pd.to_datetime(current_time).hour  
    current_date = pd.to_datetime(current_date).dayofweek 

    distances, indices = model.kneighbors([current_location])
    nearest_clusters = indices.flatten()

    filtered_data = historical_data[(historical_data['hour'] == current_time) & (historical_data['weekday'] == current_date)]
    ranked_clusters = filtered_data[filtered_data['cluster'].isin(nearest_clusters)].groupby('cluster').size().reset_index(name='count')
    ranked_clusters = ranked_clusters.sort_values(by='count', ascending=False).head(5)

    recommended_locations = pd.merge(ranked_clusters, cluster_data, on='cluster', how='left')

    recommended_locations['address'] = recommended_locations.apply(lambda row: get_location_details(row['pickup_latitude'], row['pickup_longitude']), axis=1)
    recommended_locations['distance_km'] = recommended_locations.apply(lambda row: geodesic(current_location, (row['pickup_latitude'], row['pickup_longitude'])).kilometers, axis=1)
    recommended_locations['distance_km'] = round(recommended_locations['distance_km'],1)
    # Calculate scores
    recommended_locations['distance_score'] = 1 - (recommended_locations['distance_km'] / avg_distance_all_hotspots)
    recommended_locations['distance_score'] = round(recommended_locations['distance_score'],2)*100
    max_count = ranked_clusters['count'].max()
    recommended_locations['popularity_score'] = recommended_locations['count'] / max_count
    recommended_locations['popularity_score'] = round(recommended_locations['popularity_score'],2)*100
    recommended_locations['recommendation_score'] = (recommended_locations['distance_score'] + recommended_locations['popularity_score']) / 2
    recommended_locations['recommendation_score'] = round(recommended_locations['recommendation_score'],2)

    return recommended_locations.sort_values(by='recommendation_score', ascending=False)




def create_map(current_location, recommended_locations):

    map = folium.Map(location=current_location, zoom_start=12)

    folium.Marker(
        current_location, 
        popup='Current Location', 
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(map)

    for idx, row in recommended_locations.iterrows():
        popup_info = f"{idx+1}. {row['address']} (Distance: {row['distance_km']:.2f} km)"
        folium.Marker(
            [row['pickup_latitude'], row['pickup_longitude']],
            popup=popup_info,
            icon=folium.Icon(color='blue', icon='star')
        ).add_to(map)

    return map

 


# Streamlit UI
st.set_page_config(page_title="Taxi Pickup Location Recommender", layout="wide")
st.sidebar.header("Recommender")

# Custom CSS
st.markdown("""
             <style>
             .title {
                 padding: 10px 15px;
                 border-radius: 2px;
             }
             .title h1 {
                 color: #FFAC2F;
                 font-size: 60px;
                 font-family:impact;
             }
             </style>
             """, unsafe_allow_html=True)

st.markdown('<div class="title"><h1>Where is Your Next Pickup Location?</h1></div>', unsafe_allow_html=True)
st.markdown("### Enter your current location and select the time and day to get taxi pickup recommendations.")
st.markdown('📢 _Currently the recommended locations are limited to Chicago, US. We are working in progress to collect more trip data to train our model to make recommendations in more extensive regions with accurate information._')

# Input for location
col1, col2 = st.columns(2)
with col1:
    latitude = st.number_input("Latitude", value=41.899602, format="%.6f", step=0.000001)
with col2:
    longitude = st.number_input("Longitude", value=-87.633308, format="%.6f", step=0.000001)
current_location = (latitude, longitude)

# Define the timezone and get current time
timezone = pytz.timezone('America/Chicago')
current_datetime = datetime.now(timezone)
current_hour = current_datetime.hour
current_weekday = current_datetime.strftime('%A')

# Input for time
col3, col4 = st.columns(2)
with col3:
    # Set the default to current hour
    current_time = st.slider("Time (24-hour format)", 0, 23, current_hour)
with col4:
    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    current_day = st.selectbox("Day", days_of_the_week, index=days_of_the_week.index(current_weekday))

# Button to recommend pickup locations
if st.button('Recommend Pickup Locations'):
    days = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    current_day_num = days[current_day]
    
    # Assuming your recommend_pickup_locations and create_map functions are defined as before

    recommended_pickups = recommend_pickup_locations(current_location, current_time, current_day_num, loaded_nearest_neighbors, cluster_centers, trips)
    
    if not recommended_pickups.empty:
        st.write(recommended_pickups[['recommendation_score','address', 'distance_km','distance_score','popularity_score','pickup_latitude','pickup_longitude']])
        pickup_map = create_map(current_location, recommended_pickups)
        folium_static(pickup_map)
        

        
    else:
        st.write("No recommendations available for the given input.")