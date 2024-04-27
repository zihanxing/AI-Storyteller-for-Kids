import streamlit as st
import time
from PIL import Image
import streamlit.components.v1 as components
import io
import requests
import base64
from streamlit_mic_recorder import speech_to_text
from tools.storyteller import ask_question, story_trunks
from tools.helper import autoplay_audio
from tools.text2speech import get_speech_from_text
import json
import os


API_TOKEN="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"
API_URL_disney = "https://api-inference.huggingface.co/models/ZachX/disney_SDXL_lora"
API_URL_comics = "https://api-inference.huggingface.co/models/ZachX/comics_SDXL_lora"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload, API_URL):
    """
    Query the Lora model with the payload
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def pil_to_image(images):
    """
    Convert PIL images to base64 strings
    """
    image_base64=[]
    for img in images:
        img_byte_arr = io.BytesIO() 
        img.save(img_byte_arr, format='PNG') 
        img_byte_arr = img_byte_arr.getvalue() 
        img_base64 = base64.b64encode(img_byte_arr).decode()
        image_base64.append(img_base64)
    return image_base64


def generate_slides_html(base64_string_image_folder):
    """
    Generate HTML for the slides
    """
    slides_html = ""
    i=0
    for base64_string in base64_string_image_folder:
        
        slide = f"""
        <div class="mySlides fade">
            <div class="numbertext">{i + 1} / {len(base64_string_image_folder)}</div>
            <img src="data:image/jpeg;base64,{base64_string}" style="width: 600px; height: 600px;">
            <div class="text">Caption for </div>
        </div>
        """
        slides_html += slide
        i+=1
    return slides_html

def display_tell_story(chunk_prompt, style, API_URL=API_URL_disney):
    """
    Display the story with images (with desired style) and audio
    """
    images=[]
    chunk=[]
    
    progress_text = "Generating the Story 💨"
    my_bar = st.progress(0, text=progress_text)

    for i, item in enumerate(chunk_prompt):
        my_bar.progress(int((i+1)/len(chunk_prompt)*100), text=progress_text)
    # for item in chunk_prompt:
        temp_query=query({"inputs":f'{style} style' + item[1]}, API_URL)
        images.append(Image.open(io.BytesIO(temp_query)))
        chunk.append(item[0])

    image_base64=pil_to_image(images)
    slides_html=generate_slides_html(image_base64)
    print(f"image_base64:{len(image_base64)}")
    
    story = " ".join(chunk)
    duration = {}
    for i, text in enumerate(chunk):
        duration[i] = len(text.split(" "))/30*12000

    print(f"Duration: {duration}, Type: {type(duration)}")
    duration = json.dumps(duration)
    print(f"Duration: {duration}, Type: {type(duration)}")
    
    get_speech_from_text(story ,'story')
    autoplay_audio('./assets/story.mp3')
    
    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        * {{box-sizing: border-box;}}
        body {{font-family: Verdana, sans-serif;}}
        .mySlides {{display: none;}}
        img {{vertical-align: middle;}}

        /* Slideshow container */
        .slideshow-container {{
        max-width: 1000px;
        position: relative;
        margin: auto;
        }}

        /* Caption text */
        .text {{
        color: #f2f2f2;
        font-size: 15px;
        padding: 8px 12px;
        position: absolute;
        bottom: 8px;
        width: 100%;
        text-align: center;
        }}

        /* Number text (1/3 etc) */
        .numbertext {{
        color: #f2f2f2;
        font-size: 12px;
        padding: 8px 12px;
        position: absolute;
        top: 0;
        }}

        /* The dots/bullets/indicators */
        .dot {{
        height: 15px;
        width: 15px;
        margin: 0 2px;
        background-color: #bbb;
        border-radius: 50%;
        display: inline-block;
        transition: background-color 0.6s ease;
        }}

        .active {{
        background-color: #717171;
        }}

        /* Fading animation */
        .fade {{
        animation-name: fade;
        animation-duration: 1.5s;
        }}

        @keyframes fade {{
        from {{opacity: .4}} 
        to {{opacity: 1}}
        }}

        /* On smaller screens, decrease text size */
        @media only screen and (max-width: 300px) {{
        .text {{font-size: 11px}}
        }}
        </style>
        </head>
        <body>

        <h2>Automatic Slideshow</h2>

        <div class="slideshow-container"> 
            {slides_html}
        </div>
        <br>

        <script>
        let slideIndex = 0;
        var duration = { duration };
        console.log(duration['0']);
        console.log(duration[1]);
        console.log(duration[2]);
        
        showSlides();
        
        function showSlides() {{
        let i;
        let slides = document.getElementsByClassName("mySlides");
        let dots = document.getElementsByClassName("dot");
        for (i = 0; i < slides.length; i++) {{
            slides[i].style.display = "none";  
        }}
        slideIndex++;

        slides[slideIndex-1].style.display = "block";  

        setTimeout(showSlides, duration[slideIndex-1]); // Change image every 5 seconds
        }}
        </script>
        </body>
        </html> 

            """,
        height=600,
    )

def tell_story():
    """
    Play the story
    """
    img_path = "assets/pics/"
    st.audio("assets/example.mp3", format='audio/mp3')

##################
## Streamlit UI ##
##################
st.write(os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"])
st.header("Imaginative Tales📚")
st.subheader("💫 An AI Storyteller for Kids with Visual Narratives💫")
st.write("Hi there! I am your AI Storyteller. I can narrate stories with visual narratives. \
         \n 🚀 Please follow the steps below to listen to a story: \
         \n 1. Click on 'Disney Style!' or 'DC comics Style!' to choose the style of the story. \
         \n 2. Click on 'Let me know more about you😊' and answer the question. If you don't want to answer, click on 'Do it Again🔄' to get a new question. \
         \n 3. Click on 'Listen To A Story📖' to listen to the story. ")

if 'show_html' not in st.session_state:
    st.session_state.show_html = False
if 'ans' not in st.session_state:
    st.session_state.ans = ""
if 'question' not in st.session_state:
    st.session_state.question = ""
if 'log' not in st.session_state:
    st.session_state.log = []

# Determine the style of images to be generated
style = ""
col3, col4 = st.columns(2)
with col3:
    if st.button('Disney Style!'):
        style = "disney"
with col4:
    if st.button("DC comics Style!"):
        style = "dc comics"


# Display content in two buttons
col1, col2 = st.columns(2)
with col1:
    if st.button('Listen To A Story 📖'):
        st.session_state.show_html = True
with col2:
    if st.button("Do it Again 🔄"):
        st.session_state.show_html = False


# Display different content based on the session_state
if  st.session_state.show_html:
    with st.spinner('Generating Prompts...💪🏻'):
        time.sleep(5)
        chunk_prompt = story_trunks(st.session_state.question, 
                                    st.session_state.ans,
                                    st.session_state.log)
    # st.write(chunk_prompt)
    display_tell_story(chunk_prompt, style, API_URL_disney if style == "disney" else API_URL_comics)
    del st.session_state["show_html"]
    # st.ballons()
else:
    st.session_state.question, st.session_state.log = ask_question()
    st.write(st.session_state.question)
    ans = speech_to_text(language='en',start_prompt="Let me know more about you😊",
                        use_container_width=True,just_once=True,key='ANS')
        
    if ans:
        st.session_state.ans = ans
        st.write("Now Let's Listen to a Story 🥳")
    del st.session_state["show_html"]


# tell_story()

