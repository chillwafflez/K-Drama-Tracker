import requests
from bs4 import BeautifulSoup
from time import sleep
import random
import csv
import psycopg2
import psycopg2.pool
from dotenv import load_dotenv
import os
import re

def get_connection():
    try:
        load_dotenv() 
        print("Connecting to PostgreSQL database...")

        conn = psycopg2.connect(host = os.environ.get("DB_HOST"),
                                database = os.environ.get("DB_NAME"),
                                user = os.environ.get("DB_USER"),
                                password = os.environ.get("DB_PASSWORD"))
        print(f"Successfully connected")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_pool():
    try:
        load_dotenv()
        print("Creating connection pool (min = 2, max = 3)")
        
        pool = psycopg2.pool.SimpleConnectionPool( 
            2, 3, user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD"), 
            host=os.environ.get("DB_HOST"), port='5432', database=os.environ.get("DB_NAME"))
        print(f"Successfully connected!")
        return pool
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def scrape_page_completedSK(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    URL = "https://mydramalist.com"

    # ---------- Get Information from Left Side of Page ----------- #
    left_side = soup.find("div", class_="col-lg-8 col-md-8 col-rightx")

    # Get title
    title = left_side.find("h1", class_="film-title").find("a").text if left_side.find("h1", class_="film-title").find("a") else "N/A"
    print(f"TITLE: {title}")

    # Get title with year
    year_str = left_side.find("h1", class_="film-title").contents[-1]
    year = int(year_str.replace('(', "").replace(')', "").strip())
    print(f"YEAR: {year}")

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
    
    # Get Related content if there is any
    prequel_str = ""
    compilation_str = ""
    sequel_str = ""
    spinoff_str = ""
    prequel_str, compilation_str, sequel_str, spinoff_str, related_content_exists = get_related_content(extra_info, prequel_str, compilation_str, sequel_str, spinoff_str)
    if related_content_exists:
        print("RELATED CONTENT:")
        print(f"PREQUEL STRING: {prequel_str}")   
        print(f"COMPILATION STRING: {compilation_str}")   
        print(f"SEQUEL STRING: {sequel_str}") 
        print(f"SPINOFF STRING: {spinoff_str}") 

    # loop through all list items of class list-item p-a-0 to get: native title, other names
    native_title = ""
    other_names_list = []
    other_names_str = ""
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
    duration = 0
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
                hour = 0
                min = 0
                duration_str = list_item.contents[-1].strip()
                duration_str = duration_str.rstrip('.').split('.')
                if len(duration_str) == 2:
                    hour = int(duration_str[0].split()[0])
                    min = int(duration_str[1].split()[0])
                else:
                    min = int(duration_str[0].split()[0])
                duration = (hour * 60) + min

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
    print(f"NETWORK STRING: {network_string}")

    genre_string = ""
    if len(genres) != 0:
        for i in range(len(genres)):
            if i == len(genres) - 1:
                genre_string += genres[i]
            else:
                genre_string += genres[i] + ","
    print(f"GENRE STRING: {genre_string}")

    tag_string = ""
    if len(tags) != 0:
        for i in range(len(tags)):
            if i == len(tags) - 1:
                tag_string += tags[i]
            else:
                tag_string += tags[i] + ","
    print(f"TAG STRING: {tag_string}")

    with open("./data/completed_SK_extra_info.csv", mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([title, year, mdl_id, network_string, genre_string, tag_string, cast_url])
    
    # Save drama's related content if there is any
    if related_content_exists:
        with open("./data/completed_SK_related.csv", mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([title, year, mdl_id, prequel_str, compilation_str, sequel_str, spinoff_str])

    # Save cover to folder
    # cleaned_title = title.replace(" ", "").replace("'", "").replace("\"", "")
    cleaned_title = re.sub(r'[^\w.-]', '', title)
    cleaned_title = cleaned_title.replace('_', '')
    cover_path = "data/completed_SK_covers/" + cleaned_title + "_" + str(year) + "_" + str(mdl_id) + ".jpg"
    with open(cover_path, 'wb') as f:
        response = requests.get(cover_link)
        f.write(response.content)
    print(f"COVER PATH: {cover_path}")

    scraped_dict = {}
    scraped_dict['mdl_id'] = mdl_id
    scraped_dict['title'] = title
    scraped_dict['native_title'] = native_title
    scraped_dict['other_names'] = other_names_str
    scraped_dict['mdl_rating'] = mdl_rating
    scraped_dict['synopsis'] = show_synopsis
    scraped_dict['ep_count'] = episode_count
    scraped_dict['duration'] = duration
    scraped_dict['content_rating'] = content_rating
    scraped_dict['country'] = country
    scraped_dict['air_date'] = air_dates
    scraped_dict['airing'] = airing
    scraped_dict['air_year'] = year
    scraped_dict['cover_path'] = cover_path
    return scraped_dict

def get_related_content(root_element, prequel_str, compilation_str, sequel_str, spinoff_str):
    URL = "https://mydramalist.com"
    related_content_exists = False
    related_content_li = root_element.find("li", class_="list-item p-a-0 m-b-sm related-content")
    if related_content_li:
        related_content_exists = True
        related_content_divs = related_content_li.find_all("div", class_="title")
        for div in related_content_divs:
            related_content_link = URL + div.find("a").get('href')
            related_content_title = div.find("a").get('title').strip()
            content_type = div.contents[-1].strip()
            content_type = content_type.replace('(', "").replace(')', "").split()[1]            
            if content_type == 'prequel':
                prequel_str += related_content_title + '||' + related_content_link + ',,'
            elif content_type == 'compilation':
                compilation_str += related_content_title + '||' + related_content_link + ',,'
            elif content_type == 'sequel':
                sequel_str += related_content_title + '||' + related_content_link + ',,'
            elif content_type == 'spinoff':
                spinoff_str += related_content_title + '||' + related_content_link + ',,'
    if related_content_exists:
        prequel_str = prequel_str.rstrip(',,')
        compilation_str = compilation_str.rstrip(',,')
        sequel_str = sequel_str.rstrip(',,')
        spinoff_str = spinoff_str.rstrip(',,')
    return prequel_str, compilation_str, sequel_str, spinoff_str, related_content_exists

# Move data to database / create record in drama table for drama
def to_db(drama_data):
    conn = get_connection()
    cursor = conn.cursor()
    mdl_id, title, native_title, other_names_str, mdl_rating = drama_data['mdl_id'], drama_data['title'], drama_data['native_title'], drama_data['other_names'], drama_data['mdl_rating']
    synopsis, ep_count, duration, content_rating = drama_data['synopsis'], drama_data['ep_count'], drama_data['duration'], drama_data['content_rating']
    country, air_date, air_year, airing, cover_path = drama_data['country'], drama_data['air_date'], drama_data['air_year'], drama_data['airing'], drama_data['cover_path']

    title = title.replace("'", "''")
    native_title = native_title.replace("'", "''")
    other_names_str = other_names_str.replace("'", "''")
    synopsis = synopsis.replace("'", "''")

    temp1 = "INSERT INTO drama(mdl_id, title, native_title, other_names, mdl_rating, synopsis, episode_count, duration, content_rating, country, air_date, air_year, airing, cover_path) "
    temp2 = f"VALUES ({mdl_id}, '{title}', '{native_title}', '{other_names_str}', '{mdl_rating}', '{synopsis}', {ep_count}, {duration}, '{content_rating}', '{country}', '{air_date}', {air_year}, '{airing}', '{cover_path}');"
    sql = temp1 + temp2
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

def main():
    # drama_links = open("data/completed_SK_links.txt", "r") 
    # # test_link = drama_links.readline().strip()  
    # # test_link = "https://mydramalist.com/728827-land"
    # # test_link = "https://mydramalist.com/705857-umbrella"
    # # test_link = "https://mydramalist.com/702267-weak-hero"
    # # test_link = "https://mydramalist.com/710963-yeonhwa-palace"
    # # test_link = "https://mydramalist.com/57173-hospital-playlist-2" # multiple related content (compilation)

    path = "data/completed_SK_links.txt"
    with open(path, 'r') as f:
        for i, line in enumerate(f):
            if i == 10:
                break
            link = line.strip()
            print(f"{i} | {link}")
            data = scrape_page_completedSK(link)
            to_db(data)

main()

def testing():
    with open("data\completed_SK_links.txt", 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            link = lines[i].rstrip()
            print(link)
            sleep(random.randint(3,10))

