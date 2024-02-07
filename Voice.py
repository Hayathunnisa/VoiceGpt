import streamlit as st
import speech_recognition as sr
import pyttsx3
import openai

# Assign OpenAI API key
openai.api_key = "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"

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set up Streamlit for audio playback
st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to handle user input and generate response
def process_user_input():
    # Create speech recognizer object
    r = sr.Recognizer()

    # Listen for input
    with sr.Microphone() as source:
        st.write("Speak now:")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        # Recognize the audio using Google Speech Recognition
        user_input = r.recognize_google(audio, language="en-EN")
        st.write("You asked:", user_input)

        # Use OpenAI to create a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=300
        )

        # Get the response text
        response_text = response['choices'][0]['message']['content'].strip('\n\n')

        # Speak the response
        st.write("Assistant:", response_text)
        engine.say(response_text)
        engine.runAndWait()

        return user_input, response_text

    except sr.UnknownValueError:
        st.write("Sorry, I couldn't understand the audio.")
        return None, None
    except sr.RequestError as e:
        st.write(f"Speech Recognition request failed: {e}")
        return None, None
    except Exception as e:
        st.write(f"An error occurred: {e}")
        return None, None

# Main Streamlit app
def main():
    st.title("Voice Assistant with GPT-3.5 Turbo")

    while True:
        user_input, response_text = process_user_input()

        if user_input is not None:
            st.write("Conversation History:")
            st.write(f"User: {user_input}")
            st.write(f"Assistant: {response_text}")

            # Ask the user if they want to continue the conversation
            continue_conversation = st.button("Continue Conversation")
            if not continue_conversation:
                st.write("Conversation ended.")
                break

# Run the Streamlit app
if __name__ == "__main__":
    main()
