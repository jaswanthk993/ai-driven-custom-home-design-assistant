# ai-driven-custom-home-design-assistant

# AI-Driven Custom Home Design Assistant - Documentation

## Overview
The **AI-Driven Custom Home Design Assistant** is a web-based tool powered by **Google's Generative AI (Gemini)**. It generates **personalized home designs** based on user inputs such as **number of bedrooms, bathrooms, architectural style, and special features**. The tool supports three different scenarios:
1. **Real Estate Development** – Generate home designs for potential buyers.
2. **Home Renovation Services** – Provide remodeling proposals for existing homes.
3. **Architectural Firms** – Assist in creating preliminary design drafts for clients.

## Features
✅ **Text-Based Home Design Plans** – Generates a written design concept using AI.
✅ **AI-Generated Home Design Images** – Creates a visual representation of the proposed design.
✅ **Interactive Web Interface** – Built using **Streamlit** for easy user interaction.
✅ **Customizable Inputs** – Users can specify various home attributes such as size, style, and special amenities.
✅ **Google Generative AI Integration** – Utilizes **Gemini Pro** and **Gemini Pro Vision** for advanced AI-generated outputs.

---
## Setup & Installation

### Prerequisites
- Python **3.8+**
- Google API Key for Generative AI
- Streamlit Cloud (for deployment, optional)

### Clone the Repository
```bash
git clone https://github.com/jaswanthk993/ai-driven-custom-home-design-assistant.git
cd ai-driven-custom-home-design-assistant
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Up API Key
Create a `.env` file in the project directory and add your **Google API Key**:
```plaintext
GOOGLE_API_KEY=your_google_api_key_here
```

### Run the Application Locally
```bash
streamlit run app.py
```

---
## Functionality Breakdown

### 1. **User Input Form (Sidebar)**
Users input their **home design preferences**, including:
- Number of bedrooms & bathrooms
- Architectural style (e.g., Modern, Traditional, Minimalist)
- Special features (e.g., Pool, Home Office, Gym)

### 2. **Text-Based Home Design Plan Generation**
- The AI processes user inputs and generates a **detailed design description**.
- This is powered by **Google's Generative AI (Gemini Pro)**.

### 3. **Image-Based Home Design Generation**
- AI generates a **visual representation** of the home design.
- Uses **Gemini Pro Vision** to create realistic architectural images.

---
## Deployment on Streamlit Cloud

### 1. **Rename the Main File (If Necessary)**
Ensure your main script is named `app.py`.

### 2. **Create a `requirements.txt` File**
```plaintext
streamlit
google-generativeai
pillow
python-dotenv
```

### 3. **Push Code to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 4. **Deploy on Streamlit Cloud**
- Go to **Streamlit Cloud** (https://share.streamlit.io/)
- Click **New App** → Select your **GitHub Repository**
- Set the main file as `app.py`
- Add **API keys** to Streamlit secrets
- Deploy!

---
## Troubleshooting

### 1. **App Not Deploying on Streamlit?**
**Error:** `No file extension found in main module`
✅ Solution: Ensure the main script is named `app.py` and not `.py`.

### 2. **Google API Key Not Working?**
✅ Solution: Check if the `.env` file is correctly set up and contains a valid API key.

### 3. **Images Not Generating?**
✅ Solution: Add debug logs to check API response:
```python
print(response)
```

---
## Future Enhancements
🔹 Support for **3D Renderings** of home designs.  
🔹 Integration with **VR for immersive home walkthroughs**.  
🔹 Multi-room interior customization options.

---
 Author
👨‍💻 Dhanalakota Jaswanth Kumar**  
🔗 GitHub: [jaswanthk993](https://github.com/jaswanthk993)  
🔗 LinkedIn: [Jaswanth Kumar](https://www.linkedin.com/in/jaswanth-kumar-)  

---
License
MIT License

