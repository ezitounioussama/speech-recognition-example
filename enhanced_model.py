import streamlit as st
import speech_recognition as sr

# Initialize recognizer
r = sr.Recognizer()

# Supported speech recognition APIs
RECOGNITION_APIS = {
    "Google Speech Recognition": "google",
    "CMU Sphinx (Offline)": "sphinx"
}

# Supported languages with their corresponding language codes
LANGUAGES = {
    "English (US)": "en-US",
    "English (UK)": "en-GB",
    "French": "fr-FR",
    "Spanish": "es-ES",
    "German": "de-DE"
}

def transcribe_speech(api_choice, language):
    """Handles speech transcription using the selected API and language."""
    with sr.Microphone() as source:
        st.info("Speak now...")
        r.adjust_for_ambient_noise(source)  # Reduce background noise
        try:
            audio_text = r.listen(source, timeout=5)  # Capture audio with timeout
            st.info("Transcribing...")

            if api_choice == "google":
                text = r.recognize_google(audio_text, language=language)
            elif api_choice == "sphinx":
                text = r.recognize_sphinx(audio_text, language=language)
            else:
                text = "Selected API not supported yet."

            return text
        except sr.WaitTimeoutError:
            return "No speech detected. Please try again."
        except sr.UnknownValueError:
            return "Sorry, could not understand the audio."
        except sr.RequestError as e:
            return f"API request error: {str(e)}"

def main():
    st.title("Enhanced Speech Recognition App")

    api_choice = st.selectbox("Select Speech Recognition API", list(RECOGNITION_APIS.keys()))
    api_choice_key = RECOGNITION_APIS[api_choice]

    language_name = st.selectbox("Select Language", list(LANGUAGES.keys()))
    language = LANGUAGES[language_name]

    if st.button("Start Recording"):
        text = transcribe_speech(api_choice_key, language)
        st.write("Transcription:", text)
        # Save transcription to file (st.download_button better !!!)
        
        # if st.button("Save to File"):
        #     with open("transcription.txt", "w") as f:
        #         f.write(text)
        #     st.success("Transcription saved as 'transcription.txt'.")

if __name__ == "__main__":
    main()
