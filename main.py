import streamlit as st
import openai
import pyttsx3
import speech_recognition as sr
import threading

# Assign OpenAI API key
openai.api_key = "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"

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize SpeechRecognition
recognizer = sr.Recognizer()

# Variable to track whether the TTS engine is speaking
is_speaking = False

def recognize_audio():
    with sr.Microphone() as source:
        st.info("Speak now...")
        audio = recognizer.listen(source, timeout=10)

    try:
        st.success("Processing...")
        user_input = recognizer.recognize_google(audio, language="en-EN")
        return user_input
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand the audio.")
        return None
    except sr.RequestError as e:
        st.error(f"Speech Recognition request failed: {e}")
        return None

def generate_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7,
        max_tokens=800
    )

    return response['choices'][0]['message']['content'].strip('\n\n')

def tts_thread(response):
    global is_speaking
    engine.setProperty("rate", 150)


    if not is_speaking:
        is_speaking = True
        # Use a separate thread to speak the entire response
        engine.say(response)
        engine.runAndWait()
        is_speaking = False

def speak_response(response):
    st.write(f"Assistant: {response}")

    # Start a new thread for TTS to avoid "RuntimeError: run loop already started"
    threading.Thread(target=tts_thread, args=(response,), daemon=True).start()


def main():

    st.title("Voice Assistant")

    user_input = st.text_input("Enter your text here:")
    if st.button("Speak"):
        user_input_audio = recognize_audio()

        if user_input_audio:
            st.write(f"User: {user_input_audio}")

            response = generate_response(user_input_audio)
            speak_response(response)
            tts_thread(response)

if __name__ == "__main__":
    main()
