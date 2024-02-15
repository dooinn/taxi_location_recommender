import streamlit as st


# Streamlit app initialization and setup
st.set_page_config(page_title="Taxi Pickup Location Recommender", layout="wide")


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
st.markdown('<div class="title"><h1>How Our Recommendation Works</h1></div>', unsafe_allow_html=True)
st.image('system_operation.png', caption='Location Recommender system: How it operates')
st.markdown("Imagine you're in a big city, looking for the best places to catch a taxi. Our goal is to suggest to you the top 5 places where you're most likely to find a taxi, based on your current location and the time of day. Here's how we do it:")

st.header("1. **Finding the Nearest Hotspots:**")
st.markdown(" We look at your current location and find the closest taxi hotspots—places where taxis are often found.")

st.header("2. **Checking the Time and Day:** ")
st.markdown("The best spots for catching a taxi can change depending on the time and day. We use this information to refine our suggestions, ensuring they're relevant to your current situation.")

st.header("3. **Calculating Scores for Distance and Popularity:**")
st.markdown(
    """
   - **Distance Score:** Each hotspot gets a score based on how close it is to you. Closer locations score higher for convenience.
   - **Popularity Score:** We also score hotspots based on how busy they are, under the assumption that busier places have more taxis available.
    - **Recommendation Score:** We combine the distance and popularity scores to balance between finding a place that's easy for you to reach and one where you're likely to find a taxi.
    """
)
st.header("4. **Making Recommendations:**")
st.markdown("Based on these scores, we recommend the top 5 hotspots, aiming to offer you the best chances of finding a taxi quickly.")

st.markdown("In essence, we're using a smart system to guide you to the best taxi pickup locations, considering both how easy it is for you to get there and the likelihood of finding a taxi upon arrival.")