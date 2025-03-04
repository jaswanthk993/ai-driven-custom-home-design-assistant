import streamlit as st
import google.generativeai as genai
import os
import requests
import json
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables
load_dotenv()

# Set up Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_home_design(requirements):
    """Generates a home design plan using Google's Generative AI (Gemini Base)."""
    try:
        model = genai.GenerativeModel("gemini-1.0")  # Using Gemini Base Model
        response = model.generate_content(requirements)
        return response.text if response else "Error: Unable to generate design."
    except Exception as e:
        return f"API Error: {str(e)}"

def fetch_image(query):
    """Fetches an image from Unsplash based on the architectural style."""
    try:
        unsplash_access_key = os.getenv("UNSPLASH_ACCESS_KEY")  # Add your Unsplash API Key in .env
        url = f"https://api.unsplash.com/photos/random?query={query}&client_id={unsplash_access_key}"
        response = requests.get(url).json()
        return response.get("urls", {}).get("regular", None)
    except Exception as e:
        return None

def export_as_pdf(text, filename="design_plan.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)
    return filename

def export_as_txt(text, filename="design_plan.txt"):
    with open(filename, "w") as file:
        file.write(text)
    return filename

def export_as_json(text, filename="design_plan.json"):
    with open(filename, "w") as file:
        json.dump({"design_plan": text}, file)
    return filename

# Streamlit App UI
st.title("AI-Driven Custom Home Design Assistant")
st.write("Generate personalized home designs based on your preferences and requirements.")

# Scenario Selection
scenario = st.sidebar.radio("Select Scenario", [
    "Real Estate Development",
    "Home Renovation Services",
    "Architectural Firm"
])

# User Inputs
st.sidebar.header("Input Your Home Preferences")
num_bedrooms = st.sidebar.number_input("Number of Bedrooms", min_value=1, max_value=10, value=3)
num_bathrooms = st.sidebar.number_input("Number of Bathrooms", min_value=1, max_value=10, value=2)
architectural_style = st.sidebar.selectbox("Architectural Style", ["Modern", "Traditional", "Contemporary", "Minimalist", "Colonial"])
custom_features = st.sidebar.text_area("Special Features (e.g., Pool, Home Office, Gym)")
submit = st.sidebar.button("Generate Design")

if submit:
    user_requirements = (
        f"Scenario: {scenario}. Design a home with {num_bedrooms} bedrooms, "
        f"{num_bathrooms} bathrooms, style: {architectural_style}, features: {custom_features}."
    )
    
    design_plan = generate_home_design(user_requirements)
    st.subheader("Generated Home Design Plan")
    st.write(design_plan)
    
    # Fetch an image based on architectural style
    image_url = fetch_image(architectural_style)
    if image_url:
        st.image(image_url, caption=f"Example of {architectural_style} style", use_column_width=True)
    else:
        st.warning("No relevant image found.")
    
    # Export Options
    st.subheader("Export Your Design Plan")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Download as PDF"):
            pdf_file = export_as_pdf(design_plan)
            st.download_button("Download PDF", open(pdf_file, "rb"), file_name="design_plan.pdf")
    with col2:
        if st.button("Download as TXT"):
            txt_file = export_as_txt(design_plan)
            st.download_button("Download TXT", open(txt_file, "rb"), file_name="design_plan.txt")
    with col3:
        if st.button("Download as JSON"):
            json_file = export_as_json(design_plan)
            st.download_button("Download JSON", open(json_file, "rb"), file_name="design_plan.json")
