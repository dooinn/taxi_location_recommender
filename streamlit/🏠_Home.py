import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Taxi Pickup Location Recommender System",
    page_icon="🚖"
)


st.markdown("""
             <style>
             .title {
                 padding: 10px 15px;
                 border-radius: 2px;
             }
             .title h1 {
                 color: #FFAC2F; 
                 font-size: 60px;  
                 font-family: impact;
                 }
            .title h2 {
                 font-family: impact;
             """, unsafe_allow_html=True)

# Custom title with HTML and CSS
st.markdown('<div class="title"><h1>Taxi Pickup Location Recommender System</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="title"><h2>"How to find passengers in the most efficient way?"</h2></div>', unsafe_allow_html=True)

st.image('taxIDriver.jpeg')


# Introduction section
st.header("Introduction")
st.write("""
The urban transportation landscape is experiencing a significant transformation, driven by advancements in technology and data analytics. In this context, taxi services are seeking innovative solutions to enhance operational efficiency and customer satisfaction. The Taxi Pickup Location Recommender System project is a pioneering initiative aimed at addressing one of the most pressing challenges faced by taxi drivers in Chicago: identifying the most probable locations for passenger pickups with minimal effort and time. This system leverages extensive data analysis and machine learning algorithms to recommend optimal pickup points, thereby streamlining the taxi service process and improving the overall experience for both drivers and passengers.
""")

# Goal section
st.header("Goal")
st.write("""
Our primary goal is to harness data from various sources to empower taxi drivers with actionable insights that allow them to efficiently locate high-demand areas for passenger pickups. This, in turn, is expected to reduce idle time, lower fuel consumption, and increase the profitability of their operations. The recommender system utilizes the Nearest Neighbors algorithm with a "Ball Tree" method to analyze current location and time data, providing drivers with a ranked list of the top five pickup locations based on proximity and historical trends.
""")

# Data & Data Sources section
st.header("Data & Data Sources")
st.write("""
- **Big Query Google Cloud Platform**: Chicago Taxi Trips - This dataset serves as the backbone of the project, providing detailed records of taxi trips in Chicago, including pickup and dropoff locations, fare amounts, and trip durations. [Visit site](https://console.cloud.google.com/marketplace/product/city-of-chicago-public-data/chicago-taxi-trips?project=personal-projects-382818)
- **Wikipedia - Chicago Community Areas**: This online encyclopedia offers valuable information on Chicago's community areas, facilitating an understanding of the city's geographical and demographic layout, which is crucial for pinpointing high-demand areas for taxi pickups. [Visit site](https://en.wikipedia.org/wiki/Community_areas_in_Chicago)
- **Nominatim API - OpenStreetMap Data**: This API provides access to global geographical data, allowing for the retrieval of precise geo-coordinates and addresses for the pickup and dropoff locations identified in the taxi trip records. [Visit site](https://nominatim.org/release-docs/develop/api/Overview/)
- **Flat files from Chicago Data Portal**: Sourced from the city’s official data portal, this dataset includes detailed information on taxi vehicles and companies, such as vehicle models, fuel types, and company contact information, enriching the analysis with operational insights. [Visit site](https://data.cityofchicago.org/browse?q=taxi&sortBy=relevance)
""")
