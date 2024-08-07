import os
import time
import pyaudio
import speech_recognition as sr
import playsound
from gtts import gTTS 
import requests
import uuid
import openai
from datetime import date

openai_api_key = "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"
weather_api_key = "52b873fc352569baa5988a9896e72217"
news_api_key = "864159695c4a4cefbb9829b28b7c080b"
lang = 'en'

openai.api_key = openai_api_key

guy = ""

while True:
    def get_audio():
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                print(said)
                global guy
                guy = said

                if "Jarvis" in said:
                    new_string = said.replace("Jarvis", "")
                    new_string = new_string.strip()

                    if "date" in new_string:
                        current_date = date.today().strftime("%B %d, %Y")
                        speech = gTTS(text=f"Today's date is {current_date}", lang=lang, slow=False, tld="com.br")
                        file_name = f"Audio_{str(uuid.uuid4())}.mp3"
                        speech.save(file_name)
                        playsound.playsound(file_name, block=False)
                        time.sleep(5)

                    elif "weather" in new_string:
                        # Extract the city name from the user's command
                        city_index = new_string.lower().find("weather in") + len("weather in ")
                        if city_index != -1:
                            city = new_string[city_index:].strip()
                        else:
                            # If "weather in" is not found, default to a city (e.g., Boston)
                            city = "Boston"

                        # Construct the API URL with the dynamically obtained city
                        api_url = f"http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&appid={weather_api_key}"

                        response = requests.get(api_url)
                        data = response.json()

                        if "main" in data and "temp" in data["main"]:
                            temperature = round(data["main"]["temp"])
                            weather_description = data["weather"][0]["description"]

                            weather_response = f"The current temperature in {city} is {temperature}°C with {weather_description}."
                            speech = gTTS(text=weather_response, lang=lang, slow=False, tld="com.br")
                            file_name = f"Weather_Audio_{str(uuid.uuid4())}.mp3"
                            speech.save(file_name)
                            playsound.playsound(file_name, block=False)
                            time.sleep(5)
                        else:
                            print("Unable to fetch weather information.")

                    elif "news" in new_string:
                        # Fetch today's news headlines
                        news_url = f"http://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
                        response = requests.get(news_url)
                        data = response.json()

                        if "articles" in data and len(data["articles"]) > 0:
                            # Read the first news headline and summary
                            first_article = data["articles"][0]
                            news_title = first_article["title"]
                            news_summary = first_article["description"]

                            news_response = f"Today's top news headline is: {news_title}. Here is a summary: {news_summary}."
                            speech = gTTS(text=news_response, lang=lang, slow=False, tld="com.br")
                            file_name = f"News_Audio_{str(uuid.uuid4())}.mp3"
                            speech.save(file_name)
                            playsound.playsound(file_name, block=False)
                            time.sleep(5)
                        else:
                            print("No news articles found.")


                    else:
                        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": new_string}])
                        text = completion.choices[0].message.content
                        speech = gTTS(text=text, lang=lang, slow=False, tld="com.br")
                        file_name = f"Audio_{str(uuid.uuid4())}.mp3"
                        speech.save(file_name)
                        playsound.playsound(file_name, block=False)
                        time.sleep(5)

            except Exception as e:
                print(f"Exception: {str(e)}")

        return said

    if "stop" in guy:
        break

    get_audio()
