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
    print(show_synopsis)

    # --- Get extra info (div under show_detailsxx and right below show-synopsis) --- #
    extra_info = left_side.find("ul", class_="list m-a-0")

    # -- Get Native title, other names, or other list-item p-a-0s -- #
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
    print(f"NATIVE TITLE: {native_title}")
    print(f"OTHER NAMES: {other_names_list}")
    print(f"OTHER NAMES STRING: {other_names_str}")

    # Screenwriter
    # screen_writer = list_items_p_a_0[2].find("a").text
    # screen_writer_link = URL + list_items_p_a_0[2].find("a")['href']
    # print(f"SCREENWRITER: {screen_writer} | Link: {screen_writer_link}")

    # Director
    # director = list_items_p_a_0[3].find("a").text
    # director_link = URL + list_items_p_a_0[3].find("a")["href"]
    # print(f"DIRECTOR {director} | Link: {director_link}")

    # Genre
    genres = []
    genre_list = extra_info.find("li", class_="list-item p-a-0 show-genres")
    if genre_list:
        genre_list = genre_list.find_all("a")
        genres = [genre.text for genre in genre_list]
    print(f"GENRES: {genres}")

    # Tags
    tags = []
    tag_list = extra_info.find("li", class_="list-item p-a-0 show-tags")
    if tag_list:
        tag_list = tag_list.find_all("span")
        tags = [tag.text for tag in tag_list]
    print(f"TAGS: {tags}")

    # Get cast URL and save link to text file
    cast_url = link + "/cast"
    print(f"CAST URL: {cast_url}")
    cast_url_path = "scraped_data/completed_SK_cast.txt"
    cast_url_name = title + "|" + str(mdl_id) + "|" + cast_url + "\n"
    with open(cast_url_path, 'w', encoding="utf-8") as f:
        f.write(cast_url_name)

    # ---------- Get Information from Right Side of Page ----------- #
    right_side = soup.find("div", class_="col-lg-4 col-md-4")

    # -- Get episode count, air date, original network, and content rating
    list_m_b_0 = right_side.find("ul", class_="list m-b-0")
    list_of_details = list_m_b_0.find_all("li", class_="list-item p-a-0")

    # Name (from details window on right side)
    name = list_of_details[0].find("span").text
    print(f'NAME: {name}')

    # Country
    country = list_of_details[1].find(string=True, recursive=False).strip()
    print(f'COUNTRY: {country}')

    # Episode Count
    episode_count = list_of_details[2].text
    episode_count = int(episode_count.split()[1])
    print(f'EP COUNT: {episode_count}')

    # Air Dates
    air_dates = list_of_details[3].text
    air_dates = air_dates.split(":")[1].strip()
    print(f'AIR DATE: {air_dates}')

    # Original Network
    networks = list_of_details[5].find_all("a")
    networks = [n.text for n in networks]
    print(f"ORIGINAL NETWORKS: {networks}")

    # Duration
    duration = list_of_details[6].contents[-1]
    duration = duration.strip()
    print(f"DURATION: {duration}")

    # Content Rating
    content_rating = list_m_b_0.find("li", class_="list-item p-a-0 content-rating").text
    content_rating = content_rating.split(":")[1].strip()
    print(f"CONTENT RATING: {content_rating}")

    # Save cover to folder
    cleaned_title = title_with_year.replace(" ", "").replace("(", "-").replace(")", "")
    cover_path = "scraped_data/completed_SK_covers/" + cleaned_title + "-" + str(mdl_id) + ".jpg"
    with open(cover_path, 'wb') as f:
        response = requests.get(cover_link)
        f.write(response.content)
    print(f"COVER PATH: {cover_path}")

    # Airing
    airing = False
    print(f"AIRING: {airing}")

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
    drama_links = open("scraped_data/completed_SK_links.txt", "r") 
    # test_link = drama_links.readline().strip()  
    test_link = "https://mydramalist.com/754549-tokyo-hinkon-joshi"
    scrape_page_completedSK(test_link)

    drama_links.close()

main()