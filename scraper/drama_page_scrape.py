import requests
from bs4 import BeautifulSoup
from time import sleep
import random

URL = "https://mydramalist.com"
drama_links = open("scraped_data/completed_SK_links.txt", "r") 

test_link = drama_links.readline().strip()

page = requests.get(test_link)
soup = BeautifulSoup(page.content, "html.parser")


# Get name

# Get MDL ID
mdl_id = test_link.split()

# ---------- Get Information from Left Side of Page ----------- #
left_side = soup.find("div", class_="col-lg-8 col-md-8 col-rightx")

# Get cover
cover_link = left_side.find("img", class_="img-responsive")['src']
# with open("scraped_data/completed_SK_covers/", 'wb') as f:
#     response = requests.get(cover_link)
#     f.write(response.content)
print(f"COVER LINK: {cover_link}")

# Get Rating (div under show_detailsxx)
rating = left_side.find("div", class_="box deep-orange").text
print(f"RATING: {rating}")

# Get synopsis (div under show_detailsxx)
show_synopsis = left_side.find("div", class_="show-synopsis").find("span").text
print(show_synopsis)

# --- Get extra info (div under show_detailsxx and right below show-synopsis) --- #
extra_info = left_side.find("ul", class_="list m-a-0")

# -- Get Native title, other names, screenwriter, and director
list_items_p_a_0 = extra_info.find_all("li", class_="list-item p-a-0")

# Native title
native_title = list_items_p_a_0[0].find("a")['title']
print(f"NATIVE TITLE: {native_title}")

# Other names
other_names = []
a_hrefs_under_other_names_list_time = list_items_p_a_0[1].find_all("a")
for name in a_hrefs_under_other_names_list_time:
    other_names.append(name["title"])
print(f"OTHER NAMES: {other_names}")

# Screenwriter
screen_writer = list_items_p_a_0[2].find("a").text
screen_writer_link = URL + list_items_p_a_0[2].find("a")['href']
print(f"SCREENWRITER: {screen_writer} | Link: {screen_writer_link}")

# Director
director = list_items_p_a_0[3].find("a").text
director_link = URL + list_items_p_a_0[3].find("a")["href"]
print(f"DIRECTOR {director} | Link: {director_link}")

# Genre
genre_list = extra_info.find("li", class_="list-item p-a-0 show-genres")
genre_list = genre_list.find_all("a")
genres = [genre.text for genre in genre_list]
print(f"GENRES: {genres}")

# Tags
tag_list = extra_info.find("li", class_="list-item p-a-0 show-tags")
tag_list = tag_list.find_all("span")
tags = [tag.text for tag in tag_list]
print(f"TAGS: {tags}")

# Get cast URL  
cast_url = left_side.find("div", class_="box-footer text-center").find("a").get('href')
print(f"CAST URL: {cast_url}")

# ---------- Get Information from Right Side of Page ----------- #
right_side = soup.find("div", class_="col-lg-4 col-md-4")

# -- Get episode count, air date, original network, and content rating
list_m_b_0 = right_side.find("ul", class_="list m-b-0")
list_of_details = list_m_b_0.find_all("li", class_="list-item p-a-0")

# Name
name = list_of_details[0].find("span").text
print(f'NAME: {name}')

# Country
country = list_of_details[1].find(string=True, recursive=False)
print(f'COUNTRY: {country}')

# Episode Count
episode_count = list_of_details[2].text
print(f'EP. COUNT: {episode_count}')

# Air Dates
air_dates = list_of_details[3].text
print(f'AIR DATE: {air_dates}')

# Original Network
networks = list_of_details[5].find_all("a")
networks = [n.text for n in networks]
print(f"ORIGINAL NETWORKS: {networks}")

# Content Rating
content_rating = list_m_b_0.find("li", class_="list-item p-a-0 content-rating").text
print(f"CONTENT RATING: {content_rating}")