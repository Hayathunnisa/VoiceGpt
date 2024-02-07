import openai
import speech_recognition as sr
import pyttsx3
import threading
# Assign OpenAI API key
openai.api_key = "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"

# Initialize text-to-speech engine
engine = pyttsx3.init()

r = sr.Recognizer()

# Loop to listen for audio input
while True:

    with sr.Microphone() as source:
        print("Speak now:")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        # Recognize the audio using Google Speech Recognition
        user_input = r.recognize_google(audio, language="en-EN")
        print("You asked:", user_input)

        # Check if the termination phrase is detected
        if "close this conversation" in user_input.lower():
            print("Conversation ended.")
            break

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
        print(response_text)

        # Speak the response
        engine.say(response_text)
        engine.runAndWait()
        print()

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        print(f"Speech Recognition request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


