import telebot
import requests
import datetime as dt
from telebot import types
import json

bot = telebot.TeleBot("6186813442:AAEW5_VDtCKIam5Xih6Zq1VbJaaf-5wOSUM")

# CONSTS !!!!!!!
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
API_KEY = 'd3ebabc9202919ea26b3d919c2e02675'

with open('users_data.json', 'r') as file:
    users_data = json.load(file)


# functions

def main_reply_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("⛅️weather"), types.KeyboardButton('❓FAQ'), types.KeyboardButton('🦆about us'))
    markup.row(types.KeyboardButton("🤖about bot"), types.KeyboardButton('☎️our contacts'),
               types.KeyboardButton('/start'))
    return markup


def weather_reply_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("ex🔙"))
    return markup


def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = kelvin * (9 / 5) + 32
    return celsius, fahrenheit


def metres_per_second_to_kilometres_per_hour(speed_metres_per_second):
    return speed_metres_per_second * 3.6


def city_exists(city_name, cid):
    url = BASE_URL + "q=" + city_name + "&appid=" + API_KEY
    response = requests.get(url)
    if response.status_code == 200:  # Successful search city
        users_data[cid] = city_name
        if cid in users_data:
            users_data.pop(cid)
            users_data[cid] = city_name
            with open('users_data.json', "w", encoding='utf-8') as dump_file:
                json.dump(users_data, dump_file)
        else:
            users_data[cid] = city_name
            with open('users_data.json', "w", encoding='utf-8') as dump_file:
                json.dump(users_data, dump_file)
        return True
    else:
        return False


print('____START BOT____')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    cid = message.from_user.id
    bot.reply_to(message, "Hi! My name is alesuuuk_weather_bot.")
    bot.send_message(cid, "I can send weather data of your location and then give you advices "
                          "how you should dress up! Type weather to continue!", reply_markup=main_reply_menu())


# main fun with all functional of bot
@bot.message_handler(func=lambda message: True)
def bot_functional(message):
    cid = message.from_user.id
    if message.text == "⛅️weather":  # weather
        bot.send_message(cid, "Type your city or 'ex🔙' to exit", reply_markup=weather_reply_menu())
        bot.register_next_step_handler(message, get_weather)

    elif message.text == "❓FAQ":  # FAQ
        bot.send_message(cid, "1. I enter my city, but it does not find it?\n\n"
                              "In this case, try restarting the bot with the /start command. "
                              "If it doesn't help, make sure that you entered the settlement correctly. "
                              "If you are a foreigner, "
                              "try to enter the name of your city or village in the translator and try again. "
                              "If everything still does not help - enter another settlement, "
                              "which is close to you - perhaps your settlement is not in our database!"
                              "\n\n2.Why such limited functionality?\n\n"
                              "The story is simple! This project is being developed by just one person, "
                              "and a beginner at that! This project, "
                              "like a person, is developing - and in the future we will increase the functionality"
                              "\n\n3.Why can't I check my city?\n\nWe use API technologies, "
                              "and unfortunately they still cannot make a weather forecast for all settlements! "
                              "If you need to check the weather - type the nearest command point to yours, it can help!"
                              "\n\nIf you have other questions, write to e-mail:  aslesyk2@gmail.com\n"
                              "We will help you with your questions!")

    elif message.text == "☎️our contacts":  # giving user contacts
        bot.send_message(cid, "OUR CONTACTS:\naslesyk2@gmail.com, \n0233456785(random phone number don't call!!!!)")

    elif message.text == "🦆about us":  # telling user about me
        bot.send_message(cid, "My name is Artem Lesyk - and I am a novice programmer. "
                              "I am the only developer (not counting God's Help YT and GPT)))))")

    elif message.text == "🤖about bot":  # telling about bot
        bot.send_message(cid, "This bot - asks for your geolocation (city name) "
                              "and gives an accurate current weather forecast")
    else:
        bot.send_message(cid, "No such command found! Try again!")


def get_weather(message):  # fun for giving data weather for user
    cid = message.from_user.id
    city_name = message.text
    if city_name == "ex🔙":
        bot.send_message(cid, "You have successfully exited!", reply_markup=main_reply_menu())
        return

    url = BASE_URL + "q=" + city_name + "&appid=" + API_KEY  # getting personal url for user
    response = requests.get(url).json()

    if city_exists(city_name, cid):

        # temperature
        temp_kelvin = response['main']['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        bot.send_message(cid,
                         f"Temperature in {city_name}: {temp_celsius:.2f}° in C° or {temp_fahrenheit:.2f}°"
                         f" in F° or {temp_kelvin:.2f}° in K°")

        # feels like temperature
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        bot.send_message(cid, f"Temperature in {city_name} feels like: {feels_like_celsius:.2f}° in C° or "
                              f"{feels_like_fahrenheit:.2f}° in F° or {feels_like_kelvin:.2f}° in K°")

        # wind speed
        metres_per_second_wind_speed = response['wind']['speed']
        kilometres_per_hour_wind_speed = metres_per_second_to_kilometres_per_hour(metres_per_second_wind_speed)
        bot.send_message(cid, f"Wind speed in {city_name}: {kilometres_per_hour_wind_speed:.2f} in km/h"
                              f" or {metres_per_second_wind_speed:.2f} in m/s")

        # humidity
        humidity = response['main']['humidity']
        bot.send_message(cid, f"Humidity in {city_name}: {humidity}%")

        # description about weather
        weather_description = response['weather'][0]['description']
        bot.send_message(cid, f"General weather in {city_name}: {weather_description}")

        # sun rise and set in local time
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
        bot.send_message(cid, f"Sun rises in {city_name} at {sunrise_time} at local time")
        bot.send_message(cid, f"Sun sets in {city_name} at {sunset_time} at local time", reply_markup=main_reply_menu())

        if temp_celsius < 7:
            bot.send_message(cid, "It's quite cold outside. In order not to freeze, "
                                  "I recommend you to dress warmly, as for example in the photo:")
            photo = open("winter_below_zero.jpg", "rb")
            bot.send_photo(cid, photo)

        elif 7 < temp_celsius < 18:
            bot.send_message(cid, "It's cool outside, but it's not cold!"
                                  " You should wear something warm like this dog :)")
            photo = open('cute_warm_dog.jpeg', "rb")
            bot.send_photo(cid, photo)
        else:
            bot.send_message(cid, "It is quite warm outside, you can easily dress:")
            photo = open('summer_clothes.jpg', 'rb')
            bot.send_photo(cid, photo)
    else:
        bot.send_message(cid, "I didn't found that city or village, please try again!", reply_markup=main_reply_menu())


bot.infinity_polling()
