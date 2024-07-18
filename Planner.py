import streamlit as st
import google.generativeai as palm
# from rough import API_KEY 

# Configure the API key
filename = 'apikey'
def get_file_contents(filename):
    """ Given a filename,
        return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)
API_KEY = get_file_contents(filename)
# print("Our API key is: %s" % (api_key))

palm.configure(api_key=st.secrets["API_KEY"])

# Define the model to use 
model_name = "models/text-bison-001"  

# Introduction text
st.markdown("""
# TripTrek: Intelligent Travel Planning with AI

TripTrek is an AI-powered travel planning platform designed to revolutionize the way people plan and organize their trips. By leveraging advanced artificial intelligence algorithms, TripTrek offers users personalized travel itineraries tailored to their preferences, interests, and budget constraints. The platform combines machine learning models with rich travel data to provide users with comprehensive recommendations for accommodations, activities, dining options, transportation, and more. With TripTrek, travelers can say goodbye to the hassle of manually researching and organizing every aspect of their trip and instead enjoy a seamless and stress-free travel planning experience.

## Scenario 1: Family Vacation Coordination
TripTrek helps families plan their vacations by taking user inputs such as destination and number of days to generate a detailed itinerary. It suggests family-friendly attractions like amusement parks, museums, and scenic spots, and provides recommendations for nearby restaurants and cafes that cater to diverse dietary needs. The output is a day-by-day itinerary that includes timings for visits to attractions, meal breaks at recommended food places, and suggested activities for relaxation and entertainment, ensuring a balanced and enjoyable trip for all family members.

## Scenario 2: Business Travel Planning for Professionals
TripTrek streamlines business travel for professionals by taking user inputs like destination and number of days to create a comprehensive itinerary. It recommends key business venues such as conference centers and meeting locations, along with local attractions for downtime. Additionally, it provides suggestions for nearby restaurants and cafes suitable for business lunches and dinners. The output is a detailed day-by-day schedule that includes meeting times, locations, and meal breaks at recommended food places, helping professionals maximize their time and maintain productivity during their trip.

## Scenario 3: Educational Trip for Students
TripTrek assists in planning educational trips for students by taking inputs like destination and number of days to produce a structured itinerary. It suggests educational and historical sites, museums, universities, and science centers that align with the trip's educational goals. Furthermore, it provides recommendations for student-friendly dining options, including affordable restaurants and food courts. The output is a day-by-day itinerary that includes timings for visits to educational sites, meal breaks at recommended food places, and leisure activities, ensuring a balanced and engaging trip for students.
""")

# Streamlit App Title
st.title("AI Travel Planner Itinerary")

# User Input for Travel Destination
destination = st.text_input("Enter your Travel Destination: ",placeholder="Please enter this field")

purpose = st.selectbox("Which best describes the purpose of the trip ?",["Family","Business","Educational"])

# User Input for Number of Days
num_days = st.number_input("Enter the number of days for the trip: ",min_value=1,max_value=10,step=1)

# Button to Generate Itinerary
if st.button("Generate Itinerary"):
    # Placeholder for the generated itinerary
    itinerary = ""
    food_places = ""

    # Generate Itinerary using the selected model
    try:
        with st.spinner("Generating Itinerary..."):
            # Generate text using the model
            context = ""
            family = "You are TripTrek. TripTrek helps families plan their vacations by taking user inputs such as destination and number of days to generate a detailed itinerary. It suggests family-friendly attractions like amusement parks, museums, and scenic spots, and provides recommendations for nearby restaurants and cafes that cater to diverse dietary needs. The output is a day-by-day itinerary that includes timings for visits to attractions, meal breaks at recommended food places, and suggested activities for relaxation and entertainment, ensuring a balanced and enjoyable trip for all family members."
            business = "You are TripTrek. TripTrek streamlines business travel for professionals by taking user inputs like destination and number of days to create a comprehensive itinerary. It recommends key business venues such as conference centers and meeting locations, along with local attractions for downtime. Additionally, it provides suggestions for nearby restaurants and cafes suitable for business lunches and dinners. The output is a detailed day-by-day schedule that includes meeting times, locations, and meal breaks at recommended food places, helping professionals maximize their time and maintain productivity during their trip."
            educational = "You are TripTrek.TripTrek assists in planning educational trips for students by taking inputs like destination and number of days to produce a structured itinerary. It suggests educational and historical sites, museums, universities, and science centers that align with the trip's educational goals. Furthermore, it provides recommendations for student-friendly dining options, including affordable restaurants and food courts. The output is a day-by-day itinerary that includes timings for visits to educational sites, meal breaks at recommended food places, and leisure activities, ensuring a balanced and engaging trip for students."
            
            if purpose=="Family":
                context = family
            elif purpose == "Business":
                context = business
            elif purpose == "Educational":
                context = educational
            prompt = context + f"Generate an itinerary for a {num_days}-day trip to {destination}. Include details about nearby food places."
            response = palm.generate_text(model=model_name, prompt=prompt,max_output_tokens=8192)
            itinerary = response.result  # Adjust this based on the actual response structure
    except Exception as e:
        # Display detailed error message
        st.error(f"Error generating itinerary: {e}")
        st.exception(e)
        st.warning("Please check your inputs and try again.")
    
    # Display the generated itinerary and food places
    if itinerary:
        st.success("Itinerary generated successfully!")
        st.text_area("Generated Itinerary:", value=itinerary, height=800)
    else:
        st.warning("No itinerary generated. Please try again with different inputs.")
