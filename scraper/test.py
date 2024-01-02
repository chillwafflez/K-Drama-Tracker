import requests
from bs4 import BeautifulSoup

test_link = "https://mydramalist.com/728827-land"
# test_link = "https://mydramalist.com/44961-great-vocation" # no tags, content not yet rated
# test_link = "https://mydramalist.com/710963-yeonhwa-palace" # no other names
# test_link = "https://mydramalist.com/728827-land" # has extra list-item p-a-0 called 'Related Content'
# test_link = "https://mydramalist.com/751659-cheon-nyeon-hwa"  # no tags
# test_link = "https://mydramalist.com/754549-tokyo-hinkon-joshi" # no genre
# test_link = "https://mydramalist.com/703281-my-lady" # no score

page = requests.get(test_link)
soup = BeautifulSoup(page.content, "html.parser")

left_side = soup.find("div", class_="col-lg-8 col-md-8 col-rightx")
# --- Get extra info (div under show_detailsxx and right below show-synopsis) --- #
extra_info = left_side.find("ul", class_="list m-a-0")

# -- Get Native title, other names, or other list-item p-a-0s
list_items_p_a_0 = extra_info.find_all("li", class_="list-item p-a-0")

native_title = ""
other_names_list = []
other_names_str = ""

# loop through all list items of class list-item p-a-0
for list_item in list_items_p_a_0:
    if list_item.find("b"):
        # check their b tag to get correct data
        if list_item.find("b").text == "Native Title:":
            if list_item.find("a")['title']: native_title = list_item.find("a")['title']
        if list_item.find("b").text == "Also Known As:":
            a_hrefs_under_other_names_list_time = list_item.find_all("a")
            if a_hrefs_under_other_names_list_time:
                for name in a_hrefs_under_other_names_list_time:
                    # if there is no alternate name, then 'a_hrefs_under_other_names_list_time' is an a tag with no text inside
                    if len(name) != 0:
                        other_names_list.append(name["title"])
                        other_names_str += name["title"] + "|"


# ---------- Get Information from Right Side of Page ----------- #
right_side = soup.find("div", class_="col-lg-4 col-md-4")

# -- Get episode count, air date, original network, and content rating
list_m_b_0 = right_side.find("ul", class_="list m-b-0")
list_items_p_a_0_RIGHT_SIDE = list_m_b_0.find_all("li", class_="list-item p-a-0")

name = ""
country = ""
episode_count = 0
air_dates = ""
networks = []
duration = ""
content_rating = ""

# In this for loop, obtain: name, country, ep count, air dates, networks, duration
for list_item in list_items_p_a_0_RIGHT_SIDE:
    if list_item.find("b"): # just to make sure there is a <b> element before we get the text of it
        if list_item.find("b").text == "Drama:":
            name = list_item.find("span").text
        if list_item.find("b").text == "Country:":
            # print(list_item.find(string=True, recursive=False).strip())
            country_ = list_item.contents[1].strip()
            country = country_
        if list_item.find("b").text == "Episodes:":
            episode_count_ = list_item.text
            episode_count_ = episode_count_.split()[1]
            episode_count = int(episode_count_)
        if list_item.find("b").text == "Aired:":
            air_dates_ = list_item.text
            air_dates = air_dates_.split(":")[1].strip()
        if list_item.find("b").text == "Original Network:":
            networks_ = list_item.find_all("a")
            networks = [n.text for n in networks_ if n]
        if list_item.find("b").text == "Duration:":
            duration = list_item.contents[-1].strip()

# Content Rating
list_item_content_rating = list_m_b_0.find("li", class_="list-item p-a-0 content-rating")
if list_item_content_rating: content_rating = list_item_content_rating.text.split(":")[1].strip()

print(f'NAME: {name}')
print(f'COUNTRY: {country}')
print(f'EP COUNT: {episode_count}')
print(f'AIR DATE: {air_dates}')
print(f"ORIGINAL NETWORKS: {networks}")
print(f"DURATION: {duration}")
print(f"CONTENT RATING: {content_rating}")
        

# # Genre
# genres = []
# genre_list = extra_info.find("li", class_="list-item p-a-0 show-genres")
# if genre_list:
#     genre_list = genre_list.find_all("a")
#     genres = [genre.text for genre in genre_list]

# # Tags
# tags = []
# tag_list = extra_info.find("li", class_="list-item p-a-0 show-tags")
# if tag_list:
#     tag_list = tag_list.find_all("span")
#     tags = [tag.text for tag in tag_list]


# print(f"NATIVE TITLE: {native_title}")
# print(f"OTHER NAMES: {other_names_list}")
# print(f"OTHER NAMES STRING: {other_names_str}")
# print(f"GENRES: {genres}")
# print(f"TAGS: {tags}")

#---- old way to get native and other names ---- #

# # Native title
# native_title = list_items_p_a_0[0].find("a")['title']
# print(f"NATIVE TITLE: {native_title}")

# # Other names
# other_names_list = []
# other_names_str = ""
# a_hrefs_under_other_names_list_time = list_items_p_a_0[1].find_all("a")
# if a_hrefs_under_other_names_list_time:
#     for name in a_hrefs_under_other_names_list_time:
#         other_names_list.append(name["title"])
#         other_names_str += name["title"] + "|"
# print(f"OTHER NAMES: {other_names_list}")
# print(other_names_str)
# --    -- #


# ----- old way to get name, country, ep count, air date, networks, content rating ----- #
# # ---------- Get Information from Right Side of Page ----------- #
# right_side = soup.find("div", class_="col-lg-4 col-md-4")

# # -- Get episode count, air date, original network, and content rating
# list_m_b_0 = right_side.find("ul", class_="list m-b-0")
# list_of_details = list_m_b_0.find_all("li", class_="list-item p-a-0")

# # Name (from details window on right side)
# name = list_of_details[0].find("span").text
# print(f'NAME: {name}')

# # Country
# country = list_of_details[1].find(string=True, recursive=False).strip()
# print(f'COUNTRY: {country}')

# # Episode Count
# episode_count = list_of_details[2].text
# episode_count = int(episode_count.split()[1])
# print(f'EP COUNT: {episode_count}')

# # Air Dates
# air_dates = list_of_details[3].text
# air_dates = air_dates.split(":")[1].strip()
# print(f'AIR DATE: {air_dates}')

# # Original Network
# networks = list_of_details[5].find_all("a")
# networks = [n.text for n in networks]
# print(f"ORIGINAL NETWORKS: {networks}")

# # Duration
# duration = list_of_details[6].contents[-1]
# duration = duration.strip()
# print(f"DURATION: {duration}")

# # Content Rating
# content_rating = list_m_b_0.find("li", class_="list-item p-a-0 content-rating").text
# content_rating = content_rating.split(":")[1].strip()
# print(f"CONTENT RATING: {content_rating}")