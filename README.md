# Taxi Pickup Location Recommender System

This project is part of Ironhack and the RNCP (Répertoire National des Certifications Professionnelles, RNCP37827 - Developer in Artificial Intelligence). It involves the launch of a Taxi Pickup Location Recommender System

## Requirements & Deliverables
- [Project Management - Trello](https://trello.com/b/oCHDG1CD/rncp-taxi-location-recommender)
- [Data collection & cleaning](https://github.com/dooinn/taxi_location_recommender/blob/main/jupyter_notebook/1-Data-Collection-Storing.ipynb)
- [Data expose via API & Machine Learning](https://github.com/dooinn/taxi_location_recommender/blob/main/jupyter_notebook/2-APIDataExpose-EDA%20-MachineLearning.ipynb)
- [ER model](https://github.com/dooinn/taxi_location_recommender/blob/main/img_assets/erd.png)
- [Data sources and metadata](https://github.com/dooinn/taxi_location_recommender/tree/main/datasets)
- [Databse script](https://github.com/dooinn/taxi_location_recommender/blob/main/sql/mysql_db_tables.sql)
- [Report](https://github.com/dooinn/taxi_location_recommender/blob/main/RNCP%20-%20Dooinn%20KIM%20-%20Data%20Analytics.pdf)
- [Slides](https://github.com/dooinn/taxi_location_recommender/blob/main/slides_deck.pdf)
- [Tableau Dashboard](https://public.tableau.com/app/profile/dooinn/viz/TaxiRecommendor/Dashboard3 )

## Introduction

The urban transportation landscape is experiencing a significant transformation, driven by advancements in technology and data analytics. In this context, taxi services are seeking innovative solutions to enhance operational efficiency and customer satisfaction. The Taxi Pickup Location Recommender System project is a pioneering initiative aimed at addressing one of the most pressing challenges faced by taxi drivers in Chicago: identifying the most probable locations for passenger pickups with minimal effort and time. This system leverages extensive data analysis and machine learning algorithms to recommend optimal pickup points, thereby streamlining the taxi service process and improving the overall experience for both drivers and passengers.


## Goal
Our primary goal is to harness data from various sources to empower taxi drivers with actionable insights that allow them to efficiently locate high-demand areas for passenger pickups. This, in turn, is expected to reduce idle time, lower fuel consumption, and increase the profitability of their operations. The recommender system utilizes the Nearest Neighbors algorithm with a "Ball Tree" method to analyze current location and time data, providing drivers with a ranked list of the top five pickup locations based on proximity and historical trends.

## Data & Data Sources
- **[Big Query Google Cloud Platform](https://console.cloud.google.com/marketplace/product/city-of-chicago-public-data/chicago-taxi-trips?project=personal-projects-382818)**: Chicago Taxi Trips - This dataset serves as the backbone of the project, providing detailed records of taxi trips in Chicago, including pickup and dropoff locations, fare amounts, and trip durations.
- **[Wikipedia - Chicago Community Areas](https://en.wikipedia.org/wiki/Community_areas_in_Chicag)**: This online encyclopedia offers valuable information on Chicago's community areas, facilitating an understanding of the city's geographical and demographic layout, which is crucial for pinpointing high-demand areas for taxi pickups.
- **[Nominatim API - OpenStreetMap Data](https://nominatim.org/release-docs/develop/api/Overview/)** - This API provides access to global geographical data, allowing for the retrieval of precise geo-coordinates and addresses for the pickup and dropoff locations identified in the taxi trip records.
- **[Flat files from Chicago Data Portal](https://data.cityofchicago.org/browse?q=taxi&sortBy=relevance)** - Sourced from the city’s official data portal, this dataset includes detailed information on taxi vehicles and companies, such as vehicle models, fuel types, and company contact information, enriching the analysis with operational insights.




## Streamlit App Demonstration
<div>
    <a href="https://www.loom.com/share/9a27d4a7538848da91a404d32a4ee551">
      <p>Loom Message - 6 May 2024 - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/9a27d4a7538848da91a404d32a4ee551">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/9a27d4a7538848da91a404d32a4ee551-with-play.gif">
    </a>
  </div>


