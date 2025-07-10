import requests
import json
import streamlit as st
from pathlib import Path

# API setup for Copilot API
copilot_api_url = "https://copilot5.p.rapidapi.com/copilot"
copilot_api_key = "39cdf9f051msh87e96ec3172fba2p16c83cjsnc92d4dbc35f5"  # Updated Copilot API key

# Imgur API setup
imgur_client_id = "fef2233a2ffad44"

def save_uploaded_file(uploaded_file):
    save_dir = Path('uploaded_images')
    save_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
    file_path = save_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def upload_image_and_get_url(image_path):
    with open(image_path, "rb") as image_file:
        headers = {
            "Authorization": f"Client-ID {imgur_client_id}"
        }
        files = {
            'image': image_file
        }
        response = requests.post("https://api.imgur.com/3/upload", headers=headers, files=files)
        if response.status_code == 200:
            return response.json()['data']['link']
        else:
            st.error(f"Error uploading image to Imgur: {response.status_code} - {response.text}")
            return None

def get_copilot_response(message, image_url):
    payload = {
        "message": message,
        "conversation_id": None,
        "tone": "BALANCED",
        "markdown": False,
        "photo_url": image_url  # Provide the uploaded image URL here
    }
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "copilot5.p.rapidapi.com",
        "x-rapidapi-key": copilot_api_key
    }

    response = requests.post(copilot_api_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error: {response.status_code} - {response.text}"}

# Custom CSS to apply gradient to the title and improve overall styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d3436 100%);
        color: #ffffff;
    }
    .title {
        font-size: 3em;
        font-weight: bold;
        background: linear-gradient(
            90deg,
            #ff0080,
            #ff8c00,
            #40e0d0
        );
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 1.5em;
        color: #ffffff;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #ff0080;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff8c00;
        box-shadow: 0 5px 15px rgba(255,255,255,0.1);
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    .stFileUploader>div>div {
        border-radius: 20px;
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    .stMarkdown {
        color: #ffffff;
    }
    .stAlert {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page layout
st.markdown('<h1 class="title">Hey There, I am Lexi</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your AI-powered Image Analyst</p>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.title("Menu")
    st.info("Upload an image and ask a question about it. The app will provide answers based on the image.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add an image to the sidebar
    sidebar_image_path = "alien.png"  
    st.image(sidebar_image_path, caption="", use_column_width=True)
    

    
    # Adding a button for Text and Visual Elements Extractor in the sidebar
    
    
    # Create a button that opens a new tab for the Text and Visual Elements Extractor app
   

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.write("#### Upload an image and ask a question about its content:")
    file = st.file_uploader("Choose an image file (JPEG, JPG, PNG)", type=["jpeg", "jpg", "png"])

    if file:
        image_path = save_uploaded_file(file)
        st.image(file, width=300, caption="Uploaded Image")
        
        user_question = st.text_input('Ask a question about your image:')
        
        if user_question:
            image_url = upload_image_and_get_url(image_path)
            
            if image_url:
                with st.spinner(text="Processing your request..."):
                    response = get_copilot_response(user_question, image_url)
                    
                    if 'error' in response:
                        st.error(response['error'])
                    else:
                        message = response.get("data", {}).get("message", "No message found in the response.")
                        st.success("Response received!")
                        with st.expander("See the answer", expanded=True):
                            st.write(message)
            else:
                st.error("Failed to upload image and get URL.")
    else:
        st.info("Please upload an image to proceed.")

with col2:
    st.markdown("""
    ### How to use Lexi:
    1. Upload an image using the file uploader.
    2. Type your question about the image in the text box.
    3. Wait for Lexi to analyze and respond.
    """)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)


