import telebot
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
bot = telebot.TeleBot("6723436350:AAFvhh9-trPtWxXCdJSNxe3J99sBazkhcGA")

# Define playlist_data as a global variable
playlist_data = None
# Define search_results as a global variable
search_results = None

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global playlist_data  # Make playlist_data accessible globally
    global search_results  # Make search_results accessible globally

    if message.text.startswith('https://open.spotify.com/playlist/'):
        url = message.text

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            playlist_id = urlparse(url).path.split("/")[-1]

            response = requests.get(f"https://api.fabdl.com/spotify/get?url=https%3A%2F%2Fopen.spotify.com%2Fplaylist%2F{playlist_id}")
            playlist_data = response.json()
         
            playlist_id = playlist_data['result']['id']
            playlist_name = playlist_data['result']['name']
            playlist_owner = playlist_data['result']['owner']
            playlist_image = playlist_data['result']['image']

            num_songs = len(playlist_data['result']['tracks'])
            songs_info = playlist_data['result']['tracks']

            markup = telebot.types.InlineKeyboardMarkup()
            get_all_songs_button = telebot.types.InlineKeyboardButton(text="Get All Songs", callback_data=f"get_all_songs_{playlist_id}")
            search_song_button = telebot.types.InlineKeyboardButton(text="Search for a Song", callback_data="search_song")
            markup.row(get_all_songs_button, search_song_button)

            bot.send_photo(message.chat.id, playlist_image, caption=f"Playlist ID: {playlist_id}\nPlaylist Name: {playlist_name}\nPlaylist Owner: {playlist_owner}\nNumber of Songs: {num_songs}", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"Failed to fetch playlist, HTTP status code: {response.status_code}")
    else:
        # Check if there are ongoing search results
        if search_results:
            search_song_handler(message)
        else:
            bot.send_message(message.chat.id, "Please send a valid Spotify playlist link.")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    global search_results  # Make search_results accessible globally

    if call.data.startswith("get_all_songs"):
        playlist_id = call.data.split("_")[3]
        all_songs_info = get_all_songs_info(playlist_id)
        for song_info in all_songs_info:
            send_song_info(call.message.chat.id, song_info)
    elif call.data == "search_song":
        search_results = []  # Initialize search_results
        bot.send_message(call.message.chat.id, "Enter the name, part of the name, or artist of the song you're looking for:")
        bot.register_next_step_handler(call.message, search_song_handler)
    elif call.data == "exit_search":
        search_results = None  # Clear search_results
        bot.send_message(call.message.chat.id, "Search operation cancelled.")
    else:
        bot.send_message(call.message.chat.id, "Invalid callback data.")

def get_all_songs_info(playlist_id):
    # Implement logic to get all songs from the playlist
    # Return a list of song information (similar to songs_info in the previous code)
    return playlist_data['result']['tracks']

def send_song_info(chat_id, song_info):
    # Implement logic to send song information to the user
    # Use bot.send_photo and bot.send_audio for sending image and audio
    gid =playlist_data['result']['gid']
    song_id = song_info['id']
    song_name = song_info['name']
    song_artists = song_info['artists']
    song_image = song_info['image']
    sent_message = bot.send_photo(chat_id, song_image, caption=f"Song ID: {song_id}\nSong Name: {song_name}\nArtists: {song_artists}")
    url = f"https://api.fabdl.com/spotify/mp3-convert-task/{gid}/{song_id}"
    
    response = requests.get(url)
    data = response.json()
    tid = data.get("result", {}).get("tid")

    mp3_url = f"https://api.fabdl.com/spotify/download-mp3/{tid}"
    bot.send_audio(chat_id, mp3_url, reply_to_message_id=sent_message.message_id)
    time.sleep(1)

def search_song_handler(message):
    global search_results  # Make search_results accessible globally
    user_input = message.text

    # Implement logic to search for the song and add the result to search_results
    matching_songs = search_song(user_input)

    if matching_songs:
        search_results.extend(matching_songs)
        for found_song_info in matching_songs:
            send_song_info(message.chat.id, found_song_info)
        
        # Send a button to end the search
        markup = telebot.types.InlineKeyboardMarkup()
        exit_button = telebot.types.InlineKeyboardButton(text="End Search", callback_data="exit_search")
        markup.row(exit_button)
        bot.send_message(message.chat.id, "Do you want to end the search?", reply_markup=markup)
    else:
        # Check if the user wants to end the search
        markup = telebot.types.InlineKeyboardMarkup()
        exit_button = telebot.types.InlineKeyboardButton(text="End Search", callback_data="exit_search")
        markup.row(exit_button)
        bot.send_message(message.chat.id, "No matching songs found. Do you want to end the search?", reply_markup=markup)

def search_song(user_input):
    # Implement logic to search for the song by partial name or artist
    # Return a list of found song information or an empty list if none found
    matching_songs = []
    for song_info in playlist_data['result']['tracks']:
        if user_input.lower() in song_info['name'].lower() or any(user_input.lower() in artist.lower() for artist in song_info['artists']):
            matching_songs.append(song_info)
    return matching_songs

bot.polling()
