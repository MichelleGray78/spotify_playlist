from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DATE_TO_SEARCH = input("Which date would you like to search for? Format: YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{DATE_TO_SEARCH}")
web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")

songs = soup.find_all(name="h3", id="title-of-a-story", class_="u-line-height-125")
song_titles = [title.getText().strip("\n \t") for title in songs]

print(song_titles)

