import requests
from bs4 import BeautifulSoup

test_link = "https://mydramalist.com/44961-great-vocation"
# test_link = "https://mydramalist.com/710963-yeonhwa-palace" # no other names
# test_link = "https://mydramalist.com/728827-land" # has extra list-item p-a-0 called 'Related Content'
# test_link = "https://mydramalist.com/751659-cheon-nyeon-hwa"  # no tags
# test_link = "https://mydramalist.com/754549-tokyo-hinkon-joshi" # no genre

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

# Genre
genres = []
genre_list = extra_info.find("li", class_="list-item p-a-0 show-genres")
if genre_list:
    genre_list = genre_list.find_all("a")
    genres = [genre.text for genre in genre_list]

# Tags
tags = []
tag_list = extra_info.find("li", class_="list-item p-a-0 show-tags")
if tag_list:
    tag_list = tag_list.find_all("span")
    tags = [tag.text for tag in tag_list]


print(f"NATIVE TITLE: {native_title}")
print(f"OTHER NAMES: {other_names_list}")
print(f"OTHER NAMES STRING: {other_names_str}")
print(f"GENRES: {genres}")
print(f"TAGS: {tags}")

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