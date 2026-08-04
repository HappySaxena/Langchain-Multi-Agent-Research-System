import streamlit as st
from src.pipeline.pipeline import run_research_pipeline

from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import tempfile
import os
import io
from pydub import AudioSegment

# --------------------------------------------------
# Audio Configuration
# --------------------------------------------------
AudioSegment.converter = "ffmpeg.exe"
AudioSegment.ffprobe   = "ffprobe.exe"

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 LangChain Multi-Agent Research System")

st.markdown("""
This application performs research using **four AI agents**:

- 🔎 Search Agent
- 📖 Reader Agent
- ✍️ Writer Agent
- 📝 Critic Agent
""")

st.divider()

# --------------------------------------------------
# State Management
# --------------------------------------------------
if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""
    
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None

# --------------------------------------------------
# Input
# --------------------------------------------------
input_mode = st.radio(
    "Choose input mode",
    ["Text", "Audio"],
    horizontal=True
)

if input_mode == "Text":
    st.text_input(
        "Enter your research topic",
        key="research_topic",
        placeholder="Example: Quantum Computing in Healthcare"
    )

elif input_mode == "Audio":
    st.info("Click the microphone and record your research topic.")

    # 1. Show the microphone button
    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        key="mic"
    )
    
    # 2. Process Audio FIRST (Before drawing the text box)
    if audio:
        audio_bytes = audio["bytes"]
        current_audio_hash = hash(audio_bytes)

        if current_audio_hash != st.session_state.last_audio_hash:
            
            with st.spinner("Transcribing audio..."):
                recognizer = sr.Recognizer()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                    temp_filename = f.name

                try:
                    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
                    audio_segment.export(temp_filename, format="wav")

                    with sr.AudioFile(temp_filename) as source:
                        audio_data = recognizer.record(source)

                    transcribed_text = recognizer.recognize_google(audio_data)

                    # Update session state BEFORE the text_input is rendered
                    st.session_state.research_topic = transcribed_text
                    st.session_state.last_audio_hash = current_audio_hash
                    
                    # Refresh to show changes immediately
                    st.rerun()  

                except sr.UnknownValueError:
                    st.error("Could not understand the audio. Please try again.")
                    st.session_state.last_audio_hash = current_audio_hash 
                except sr.RequestError as e:
                    st.error(f"Speech Recognition Error: {e}")
                    st.session_state.last_audio_hash = current_audio_hash
                except Exception as e:
                    st.error(f"An error occurred processing the audio: {e}")
                    st.session_state.last_audio_hash = current_audio_hash
                finally:
                    if os.path.exists(temp_filename):
                        os.remove(temp_filename)

    # 3. Draw the Text Box AFTER audio processing is completely finished
    st.text_input(
        "Transcribed Topic (You can edit this)",
        key="research_topic",
        placeholder="Waiting for audio..."
    )
                
# Grab the current topic from state
topic = st.session_state.research_topic

if topic:
    st.info(f"Using topic: **{topic}**")

# --------------------------------------------------
# Status Box
# --------------------------------------------------
status_placeholder = st.empty()

status = {
    "search": "⏳",
    "reader": "⏳",
    "writer": "⏳",
    "critic": "⏳",
}

def render_status():
    status_placeholder.markdown(
        f"""
### 🤖 Agent Status

| Agent | Status |
|-------|--------|
| 🔎 Search Agent | {status["search"]} |
| 📖 Reader Agent | {status["reader"]} |
| ✍️ Writer Agent | {status["writer"]} |
| 📝 Critic Agent | {status["critic"]} |
"""
    )

render_status()

# --------------------------------------------------
# Callback from pipeline
# --------------------------------------------------
def update_status(step):
    if step == "search":
        status["search"] = "🔄"
    elif step == "reader":
        status["search"] = "✅"
        status["reader"] = "🔄"
    elif step == "writer":
        status["reader"] = "✅"
        status["writer"] = "🔄"
    elif step == "critic":
        status["writer"] = "✅"
        status["critic"] = "🔄"
    elif step == "done":
        status["critic"] = "✅"

    render_status()

# --------------------------------------------------
# Run Button
# --------------------------------------------------
if st.button("🚀 Start Research", use_container_width=True):

    if topic.strip() == "":
        st.warning("Please enter a research topic.")
        st.stop()

    # Reset status
    status["search"] = "⏳"
    status["reader"] = "⏳"
    status["writer"] = "⏳"
    status["critic"] = "⏳"
    render_status()

    try:
        with st.spinner("Running Multi-Agent Research Pipeline..."):
            state = run_research_pipeline(
                topic=topic,
                status_callback=update_status
            )

        st.success("Research Completed Successfully!")
        st.divider()

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🔎 Search Results",
                "📖 Scraped Content",
                "✍️ Final Report",
                "📝 Critic Feedback",
            ]
        )

        with tab1:
            st.subheader("Search Results")
            st.write(state.get("search_results", "No data"))

        with tab2:
            st.subheader("Reader Agent Output")
            st.write(state.get("scraped_content", "No data"))

        with tab3:
            st.subheader("Research Report")
            st.markdown(state.get("report", "No data"))

        with tab4:
            st.subheader("Critic Feedback")
            st.markdown(state.get("feedback", "No data"))

    except Exception as e:
        st.error("An error occurred while running the pipeline.")
        st.exception(e)