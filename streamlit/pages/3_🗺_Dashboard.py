import pandas as pd
import plotly.express as px
import streamlit as st
from folium.plugins import HeatMap
import folium




df = pd.read_csv('/Users/dooinnkim/jupyter_notebook/ironhacks/taxi_location_recommender/datasets/trips_clusters_sample.csv') 


# Load the dataset

# Ensure trip_start_timestamp is a datetime type
df['trip_start_timestamp'] = pd.to_datetime(df['trip_start_timestamp'])

# Extract month, day of the week (name), and hour
df['month'] = df['trip_start_timestamp'].dt.month
df['day_of_week'] = df['trip_start_timestamp'].dt.day_name()
df['hour'] = df['trip_start_timestamp'].dt.hour

# Create a sidebar for month selection
selected_month = st.sidebar.selectbox('Select Month', df['month'].unique())

# Filter dataset based on selected month
filtered_df = df[df['month'] == selected_month]

# Setup Streamlit app title
st.title('Dashboard for Trip Data Analysis')


# Calculate total trips counts per month
monthly_trips = df.groupby(df['trip_start_timestamp'].dt.month).size().reset_index(name='total_trips')
monthly_trips.columns = ['month', 'total_trips']

# Create a line plot
fig_monthly_trips = px.line(monthly_trips, x='month', y='total_trips', title='Total Trips Counts Per Month', markers=True)

# Add labels for clarity
fig_monthly_trips.update_layout(xaxis_title='Month', yaxis_title='Total Trips', xaxis=dict(tickmode='array', tickvals=list(range(1, 13)), ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']))

# Display the line plot in Streamlit
st.plotly_chart(fig_monthly_trips)




# Aggregate data to count trips by day and hour for filtered data
trip_counts = filtered_df.groupby(['day_of_week', 'hour']).size().reset_index(name='counts')
# Correct pivot operation for heatmap
trip_counts_pivot = trip_counts.pivot(index='day_of_week', columns='hour', values='counts').fillna(0)
# Ensure the order of days in the heatmap
ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
trip_counts_pivot = trip_counts_pivot.reindex(ordered_days)
# Generate heatmap
fig = px.imshow(trip_counts_pivot,
                labels=dict(x="Hour of Day", y="Day of Week", color="Trip Counts"),
                aspect="auto")
fig.update_layout(title='Trips Counts Heatmap by Hour and Day', xaxis_nticks=24)
# Display the heatmap in Streamlit
st.plotly_chart(fig)

# Calculate median fare by day and hour for filtered data
median_fare = filtered_df.groupby(['day_of_week', 'hour'])['trip_total'].median().reset_index(name='median_fare')
# Pivot data for heatmap format
median_fare_pivot = median_fare.pivot(index='day_of_week', columns='hour', values='median_fare').fillna(0)
median_fare_pivot = median_fare_pivot.reindex(ordered_days)
# Generate heatmap for median fares
fig_fare = px.imshow(median_fare_pivot,
                     labels=dict(x="Hour of Day", y="Day of Week", color="Median Fare"),
                     aspect="auto")
fig_fare.update_layout(title='Median Trip Fare Heatmap by Hour and Day', xaxis_nticks=24)
# Display in Streamlit
st.plotly_chart(fig_fare)

# Aggregate data to count trips by pickup address for filtered data
address_counts = filtered_df['pickup_address'].value_counts().reset_index(name='counts')
address_counts.columns = ['pickup_address', 'counts']
# Generate bar chart
fig_address = px.bar(address_counts.head(20), # Limiting to top 20 for readability
                     x='pickup_address',
                     y='counts',
                     title='Total Trips Count per Address')
# Display in Streamlit
st.plotly_chart(fig_address)
