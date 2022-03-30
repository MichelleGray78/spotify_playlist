from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

DATE_TO_SEARCH = input("Which date would you like to search for? Format: YYYY-MM-DD: ")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


response = requests.get(f"https://www.billboard.com/charts/hot-100/{DATE_TO_SEARCH}")
web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")

songs = soup.find_all(name="h3", id="title-of-a-story", class_="u-line-height-125")
song_titles = [title.getText().strip("\n \t") for title in songs]

song_uris = []
year = DATE_TO_SEARCH.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{DATE_TO_SEARCH} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)