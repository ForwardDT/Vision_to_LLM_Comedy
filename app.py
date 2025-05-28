import os
from pathlib import Path
import io
import streamlit as st
from dotenv import load_dotenv
from transformers import pipeline
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from groq import Groq
from gtts import gTTS  # fallback TTS

# Load environment variables from .env
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(env_path)

# Retrieve API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Ensure env var is named GROQ_API_KEY
if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY environment variable")

# Initialize Groq client for TTS with API key
groq_client = Groq(api_key=GROQ_API_KEY)

# Initialize the image-to-text pipeline once
image_to_text_pipeline = pipeline(
    "image-to-text", model="Salesforce/blip-image-captioning-base"
)


def img2text(image_path: str) -> str:
    result = image_to_text_pipeline(image_path)
    return result[0]["generated_text"]


def strip_before_colon(text: str) -> str:
    idx = text.find(':')
    return text[idx+1:].strip() if idx != -1 else text.strip()


def generate_story(topic: str) -> str:
    chat = ChatGroq(
        temperature=1,
        api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",
        verbose=True
    )
    prompt = ChatPromptTemplate.from_messages([
        ("user", "You are a stand-up comedian, similar to Bill Burr. Generate a short (max 60 words), funny story based on: {topic}.")
    ])
    story = ""
    for chunk in (prompt | chat).stream({"topic": topic}):
        story += chunk.content
    return strip_before_colon(story)


def text2speech_bytes(message: str) -> (bytes, str):
    """
    Generate speech audio bytes from text using Groq TTS, silently fallback to gTTS.
    """
    try:
        response = groq_client.audio.speech.create(
            model="playai-tts",
            voice="Aaliyah-PlayAI",
            response_format="wav",
            input=message,
        )
        # Attempt to extract raw bytes
        audio_bytes = None
        if hasattr(response, 'binary'):
            audio_bytes = response.binary
        elif hasattr(response, 'data'):
            audio_bytes = response.data
        elif hasattr(response, 'content'):
            audio_bytes = response.content
        if not audio_bytes:
            # Fallback if attribute missing
            audio_bytes = response.read() if hasattr(response, 'read') else response.__dict__.get('binary', b'')
        return audio_bytes, 'audio/wav'
    except Exception:
        # silent fallback to gTTS
        buf = io.BytesIO()
        tts = gTTS(message)
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.getvalue(), 'audio/mpeg'


def main():
    st.set_page_config(page_title="Image to Audio Story")
    st.header("Turn an image into an audio story")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if not uploaded_file:
        return

    # Display the image
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    # Save to temp file for pipeline
    img_path = Path(uploaded_file.name)
    img_path.write_bytes(uploaded_file.getvalue())

    # Generate scenario and story
    scenario = img2text(str(img_path))
    story = generate_story(scenario)

    # Generate audio and play
    try:
        audio_data, mime = text2speech_bytes(story)
        audio_buf = io.BytesIO(audio_data)
        st.audio(audio_buf, format=mime)
    except Exception as e:
        st.error(f"Audio generation error: {e}")

    with st.expander("Scenario"):
        st.write(scenario)
    with st.expander("Story"):
        st.write(story)


if __name__ == "__main__":
    main()

