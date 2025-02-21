import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
from pydub import AudioSegment
from pydub.playback import play
import os

# Set up Gemini API Key
genai.configure(api_key="AIzaSyD15XVLBYz8uzB4qSfoTrhlfkwofXz-1UA")

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.success(f"📝 Recognized Text: {text}")
        return text
    except sr.UnknownValueError:
        st.error("❌ Could not understand the audio")
        return None
    except sr.RequestError:
        st.error("❌ API unavailable")
        return None

# Function to generate an image from text
def generate_image(text_prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content(text_prompt)

    if response and response.candidates:
        image_url = response.candidates[0].content.image_url
        return image_url
    return None

# Streamlit UI
st.title("🎨 Voice-to-Image Generator")
st.write("Speak into the microphone, and the app will generate an image based on what you said!")

# Button to record audio and generate image
if st.button("🎙️ Record and Generate Image"):
    text = recognize_speech()
    if text:
        image_url = generate_image(text)
        if image_url:
            st.image(image_url, caption="Generated Image", use_column_width=True)
        else:
            st.error("❌ Failed to generate image")

st.write("🔹 Developed with Streamlit, Google Gemini AI, and Speech Recognition.")
