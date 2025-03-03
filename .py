import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_home_design(requirements):
    """Generates a home design plan using Google's Generative AI (Gemini)."""
    model = genai.GenerativeModel("gemini-pro")  # Replace with the correct Google AI model
    response = model.generate_content(requirements)
    return response.text if response else "Error: Unable to generate design."

# Streamlit App UI
st.title("AI-Driven Custom Home Design Assistant")
st.write("Generate personalized home designs based on your preferences.")

# User Inputs
st.sidebar.header("Input Your Home Preferences")
num_bedrooms = st.sidebar.number_input("Number of Bedrooms", min_value=1, max_value=10, value=3)
num_bathrooms = st.sidebar.number_input("Number of Bathrooms", min_value=1, max_value=10, value=2)
architectural_style = st.sidebar.selectbox("Architectural Style", ["Modern", "Traditional", "Contemporary", "Minimalist", "Colonial"])
custom_features = st.sidebar.text_area("Special Features (e.g., Pool, Home Office, Gym)")
submit = st.sidebar.button("Generate Design")

if submit:
    user_requirements = (
        f"Bedrooms: {num_bedrooms}, Bathrooms: {num_bathrooms}, "
        f"Style: {architectural_style}, Features: {custom_features}"
    )
    design_plan = generate_home_design(user_requirements)
    st.subheader("Generated Home Design Plan")
    st.write(design_plan)
