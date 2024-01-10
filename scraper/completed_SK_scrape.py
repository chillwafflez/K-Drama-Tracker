import requests
from bs4 import BeautifulSoup
from time import sleep
import csv


def scrape_page_completedSK(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    # ---------- Get Information from Left Side of Page ----------- #
    left_side = soup.find("div", class_="col-lg-8 col-md-8 col-rightx")

    # Get title
    title = left_side.find("h1", class_="film-title").find("a").text if left_side.find("h1", class_="film-title").find("a") else "N/A"
    print(f"TITLE: {title}")

    # Get title with year
    title_with_year = left_side.find("h1", class_="film-title").text if left_side.find("h1", class_="film-title") else "N/A"
    print(f"TITLE (with year): {title_with_year}")

    # Get MDL ID
    mdl_id = int(link.split("/")[3].split("-")[0])
    print(f"MDL ID: {mdl_id}")

    # Get cover
    cover_link = left_side.find("img", class_="img-responsive")['src']
    print(f"COVER LINK: {cover_link}")

    # Get Rating (div under show_detailsxx) | WARNING: this could be "N/A" if no rating
    mdl_rating = left_side.find("div", class_="box deep-orange").text if left_side.find("div", class_="box deep-orange") else "N/A"
    print(f"MDL RATING: {mdl_rating}")

    # Get synopsis (div under show_detailsxx)
    show_synopsis = left_side.find("div", class_="show-synopsis").find("span").text if left_side.find("div", class_="show-synopsis").find("span") else "N/A"
    print(f"SYNOPSIS: {show_synopsis}")

    # --- Get extra info (div under show_detailsxx and right below show-synopsis) --- #
    extra_info = left_side.find("ul", class_="list m-a-0")

    # -- Get Native title, other names, or other list-item p-a-0s -- #
    list_items_p_a_0_LEFT_SIDE = extra_info.find_all("li", class_="list-item p-a-0")

    native_title = ""
    other_names_list = []
    other_names_str = ""

    # loop through all list items of class list-item p-a-0 to get: native title, other names
    for list_item in list_items_p_a_0_LEFT_SIDE:
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
                            other_names_str += name["title"] + "_"
    print(f"NATIVE TITLE: {native_title}")
    print(f"OTHER NAMES: {other_names_list}")
    other_names_str = other_names_str.rstrip('_')
    print(f"OTHER NAMES STRING: {other_names_str}")

    # Genre
    genres = []
    genre_list = extra_info.find("li", class_="list-item p-a-0 show-genres")
    if genre_list:
        genre_list = genre_list.find_all("a")
        genres = [genre.text for genre in genre_list if genre]
    print(f"GENRES: {genres}")

    # Tags
    tags = []
    tag_list = extra_info.find("li", class_="list-item p-a-0 show-tags")
    if tag_list:
        tag_list = tag_list.find_all("span")
        tags = [tag.text.rstrip(",") for tag in tag_list if tag]
    print(f"TAGS: {tags}")

    # Get cast URL and save link to text file
    cast_url = link + "/cast"
    print(f"CAST URL: {cast_url}")

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
                air_dates = " ".join(air_dates.split())
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
    print(f'AIR DATE(s): {air_dates}')
    print(f"ORIGINAL NETWORKS: {networks}")
    print(f"DURATION: {duration}")
    print(f"CONTENT RATING: {content_rating}")

    # Airing
    airing = False
    print(f"AIRING: {airing}")

    # -------- Saving cast URL, genres, tags, and cover to external files --------- #

    # Save cast URL link to text file
    cast_url_path = "data/completed_SK_cast.txt"
    cast_url_name = title + "_" + str(mdl_id) + "_" + cast_url + "\n"
    with open(cast_url_path, 'a', encoding="utf-8") as f:
        f.write(cast_url_name)
    
    # Save drama's networks, genres, and tags to csv
    network_string = ""
    if len(networks) != 0:
        for i in range(len(networks)):
            if i == len(networks) - 1:
                network_string += networks[i]
            else:
                network_string += networks[i] + ","
    print(f"network string: {network_string}")

    genre_string = ""
    if len(genres) != 0:
        for i in range(len(genres)):
            if i == len(genres) - 1:
                genre_string += genres[i]
            else:
                genre_string += genres[i] + ","
    print(f"genre string: {genre_string}")

    tag_string = ""
    if len(tags) != 0:
        for i in range(len(tags)):
            if i == len(tags) - 1:
                tag_string += tags[i]
            else:
                tag_string += tags[i] + ","
    print(f"tag string: {tag_string}")

    with open("./data/completed_SK_extra_info.csv", mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([title, title_with_year, mdl_id, network_string, genre_string, tag_string, cast_url])

    # Save cover to folder
    cleaned_title = title_with_year.replace(" ", "").replace("(", "_").replace(")", "").replace("'", "")
    cover_path = "data/completed_SK_covers/" + cleaned_title + "_" + str(mdl_id) + ".jpg"
    with open(cover_path, 'wb') as f:
        response = requests.get(cover_link)
        f.write(response.content)
    print(f"COVER PATH: {cover_path}")


    # All data
    scraped_dict = {}
    scraped_dict['mdl_id'] = mdl_id
    scraped_dict['title'] = title
    scraped_dict['native_title'] = native_title
    scraped_dict['other_names'] = other_names_str
    scraped_dict['mdl_rating'] = mdl_rating
    scraped_dict['synopsis'] = show_synopsis
    scraped_dict['ep_count'] = episode_count
    scraped_dict['air_date'] = air_dates
    scraped_dict['airing'] = airing
    scraped_dict['Title'] = title
    scraped_dict['Title'] = title
    scraped_dict['link'] = link


def main():
    drama_links = open("data/completed_SK_links.txt", "r") 
    # test_link = drama_links.readline().strip()  
    test_link = "https://mydramalist.com/728827-land"
    # test_link = "https://mydramalist.com/705857-umbrella"
    # test_link = "https://mydramalist.com/702271-weak-hero-season-2"
    # test_link = "https://mydramalist.com/710963-yeonhwa-palace"
    scrape_page_completedSK(test_link)

    drama_links.close()

main()