import streamlit as st
import numpy as np
import json
import os
import zipfile
from io import BytesIO
from models.home_design_model import HomeDesignGenerator
from utils.visualization import create_floor_plan
from utils.google_services import GoogleServicesManager
from data.room_templates import ROOM_TEMPLATES, STYLE_FEATURES
from config.api_config import validate_api_keys

st.set_page_config(
    page_title="AI Home Design Generator",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

def create_design_summary(layout_data, house_size, style, requirements):
    """Create a detailed summary of the design"""
    summary = {
        "project_info": {
            "total_area": house_size,
            "style": style,
            "special_requirements": requirements
        },
        "rooms": []
    }

    for _, room in layout_data.iterrows():
        summary["rooms"].append({
            "type": room["room_type"],
            "size": int(room["size"]),
            "dimensions": {
                "width": float(room["width"]),
                "height": float(room["height"])
            }
        })

    return json.dumps(summary, indent=2)

def create_project_zip():
    """Create a ZIP file containing all project files"""
    memory_zip = BytesIO()

    with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Define project structure
        project_files = [
            ('main.py', 'main.py'),
            ('models/home_design_model.py', 'models/home_design_model.py'),
            ('utils/visualization.py', 'utils/visualization.py'),
            ('utils/google_services.py', 'utils/google_services.py'),
            ('data/room_templates.py', 'data/room_templates.py'),
            ('config/api_config.py', 'config/api_config.py'),
            ('.streamlit/config.toml', '.streamlit/config.toml')
        ]

        # Add files to ZIP
        for file_path, zip_path in project_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    zf.writestr(zip_path, f.read())

        # Add README
        readme_content = """# AI Home Design Generator

This project uses AI to generate customized floor plans based on user preferences.

## Setup Instructions
1. Install required packages: `pip install -r requirements.txt`
2. Set up environment variables:
   - GOOGLE_API_KEY: Your Google API key
3. Run the application: `streamlit run main.py`

## Project Structure
- main.py: Main Streamlit application
- models/: Contains the AI model for floor plan generation
- utils/: Utility functions for visualization and API integration
- data/: Room templates and style definitions
- config/: Configuration management
"""
        zf.writestr('README.md', readme_content)

        # Add requirements.txt
        requirements = """streamlit>=1.42.2
numpy>=2.2.3
pandas>=2.2.3
plotly>=6.0.0
scikit-learn>=1.6.1
google-api-python-client>=2.161.0
"""
        zf.writestr('requirements.txt', requirements)

    memory_zip.seek(0)
    return memory_zip.getvalue()

def main():
    st.title("🏠 AI Home Design Generator")
    st.write("Create customized floor plans using AI")

    # Initialize Google Services
    try:
        if validate_api_keys():
            google_services = GoogleServicesManager()
        else:
            st.warning("Google API key not configured. Some features may be limited.")
            google_services = None
    except Exception as e:
        st.error(f"Error initializing Google services: {str(e)}")
        google_services = None

    # Sidebar for inputs
    with st.sidebar:
        st.header("Design Preferences")

        # Basic parameters
        num_bedrooms = st.slider("Number of Bedrooms", 1, 5, 2)
        num_bathrooms = st.slider("Number of Bathrooms", 1, 4, 2)
        additional_rooms = st.slider("Additional Rooms", 0, 4, 1)

        # Calculate total rooms
        num_rooms = num_bedrooms + num_bathrooms + additional_rooms + 2  # +2 for living room and kitchen

        house_size = st.slider("House Size (sq ft)", 800, 4000, 2000, step=100)

        style = st.selectbox(
            "Architectural Style",
            ["Modern", "Traditional", "Contemporary", "Mediterranean"]
        )

        special_requirements = st.multiselect(
            "Special Requirements",
            ["Open Floor Plan", "Home Office", "Large Kitchen", "Master Suite"],
            default=["Open Floor Plan"]
        )

        generate_button = st.button("Generate Design")

    # Main content area
    if generate_button:
        with st.spinner("Generating your dream home design..."):
            try:
                # Initialize the generator
                generator = HomeDesignGenerator()

                # Generate floor plan
                layout_data = generator.generate_layout(
                    num_rooms=num_rooms,
                    num_bedrooms=num_bedrooms,
                    house_size=house_size,
                    style=style,
                    requirements=special_requirements
                )

                # Display results in columns
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.subheader("Generated Floor Plan")
                    fig = create_floor_plan(layout_data)
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.subheader("Design Details")
                    st.metric("Total Area", f"{house_size} sq ft")
                    st.metric("Bedrooms", num_bedrooms)
                    st.metric("Total Rooms", num_rooms)

                    # Show design inspiration if Google services are available
                    if google_services:
                        st.subheader("Design Inspiration")
                        inspiration = google_services.get_design_inspiration(style, "living room")
                        if inspiration:
                            st.image(inspiration['image_url'], caption=inspiration['title'])

                # Export section
                st.subheader("Export Options")
                col3, col4 = st.columns(2)

                with col3:
                    # Export floor plan data as JSON
                    design_summary = create_design_summary(layout_data, house_size, style, special_requirements)
                    st.download_button(
                        label="📥 Download Design Summary (JSON)",
                        data=design_summary,
                        file_name="floor_plan_summary.json",
                        mime="application/json"
                    )

                with col4:
                    # Export floor plan data as CSV
                    st.download_button(
                        label="📊 Download Room Data (CSV)",
                        data=layout_data.to_csv(index=False),
                        file_name="floor_plan_data.csv",
                        mime="text/csv"
                    )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    else:
        # Display placeholder/welcome message
        st.info("👈 Set your preferences in the sidebar and click 'Generate Design' to create your custom home layout")

        # Show example/preview
        st.subheader("Example Designs")
        st.image("https://placehold.co/600x400?text=Sample+Floor+Plan", caption="Sample floor plan visualization")

    # Add project download section
    st.sidebar.markdown("---")
    st.sidebar.subheader("Developer Options")
    if st.sidebar.button("📦 Download Project Files"):
        project_zip = create_project_zip()
        st.sidebar.download_button(
            label="💾 Download Complete Project",
            data=project_zip,
            file_name="ai_home_design_generator.zip",
            mime="application/zip"
        )

if __name__ == "__main__":
    main()