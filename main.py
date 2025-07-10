import requests
import json
import streamlit as st
from pathlib import Path

# API setup for Copilot API
copilot_api_url = "https://copilot5.p.rapidapi.com/copilot"
copilot_api_key = "25c40aa56fmsh12b48be18760bb1p11101ejsn4236cc697a09"

# Imgur API setup
imgur_client_id = "8be145a73ee287b"

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
            st.write(f"Error uploading image to Imgur: {response.status_code} - {response.text}")
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

# Custom CSS to apply gradient to the title
st.markdown(
    """
    <style>
    .title {
        font-size: 4em;
        font-weight: bold;
        background: radial-gradient(
            64.18% 64.18% at 71.16% 35.69%,
            #ffd6e7 0.89%,  /* Light Pink */
            #ffaad5 17.23%, /* Medium Pink */
            #ff80c4 42.04%, /* Pink */
            #ff55b3 55.12%, /* Hot Pink */
            #ff2aa2 71.54%, /* Deep Pink */
            #ff0080 100%    /* Bright Magenta */
        );
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app with sidebar

# st.sidebar.title("Instructions")
# st.sidebar.info("Upload an image and ask a question about it. The app will provide answers based on the image.")

# Add a line break
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

# Add an image to the sidebar
sidebar_image_path = "alien.png"  # Replace with your image file path
st.sidebar.image(sidebar_image_path, caption="", use_column_width=True)

# Apply the gradient to the title
st.markdown('<h1 class="title">Hey There, I am Lexi</h1>', unsafe_allow_html=True)

st.write("#### Upload an image and ask a question about its content:")

file = st.file_uploader("Choose an image file (JPEG, JPG, PNG)", type=["jpeg", "jpg", "png"])

# Image container
image_container = st.empty()

if file:
    # Display the uploaded image in a small container
    image_container.image(file, width=200, caption="Uploaded Image")  # Adjust the width as needed

    user_question = st.text_input('Ask a question about your image:')
    
    if user_question:
        # Save the uploaded image and get its path
        image_path = save_uploaded_file(file)
        
        # Get the URL of the uploaded image
        image_url = upload_image_and_get_url(image_path)
        
        if image_url:
            with st.spinner(text="Processing your request..."):
                response = get_copilot_response(user_question, image_url)
                
                if 'error' in response:
                    st.error(response['error'])
                else:
                    st.subheader("Response:")
                    st.write(response)
        else:
            st.error("Failed to upload image and get URL.")
else:
    st.info("Please upload an image to proceed.")
