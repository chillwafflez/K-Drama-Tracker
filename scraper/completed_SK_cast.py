import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from time import sleep
import random
from db_models import *


def move_to_db(actor_details, character_details, actor_picture_URL): 
    # Save cover to folder
    cleaned_first_name = actor_details['First Name'].strip().replace(" ", "")
    cleaned_last_name = actor_details['Family Name'].strip().replace(" ", "")
    birth_year = actor_details['Born'].split(',')[1].strip()
    picture_path = "data/actor_covers/" + cleaned_first_name + "__" + cleaned_last_name + "__" + birth_year + "__" + str(actor_details['MDL ID']) + ".jpg"
    with open(picture_path, 'wb') as f:
        response = requests.get(actor_picture_URL)
        f.write(response.content)
    print(f"ACTOR PICTURE PATH: {picture_path}")


    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    # test_actor = Actor(6969, "Justin", "Nguyen", "Justeen", "bruh__hi", "Vietnamese", "Male", "2003-04-28", 20, "blah blah blah", "path_blah_png")
    actor = Actor(actor_details['MDL ID'], actor_details['First Name'], actor_details['Family Name'], actor_details['Native name'], actor_details['Also Known as'], actor_details['Nationality'], actor_details['Gender'], actor_details['Born'], actor_details['Age'], actor_details['Biography'], picture_path)
    session.add(actor)
    session.commit()
    session.close()

    

# Obtain all of the actor's data, including URL to their face picture
def scrape_actor(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    mdl_id = int(link.split("/")[4].split("-")[0])
    
    left_side = soup.find("div", class_="col-lg-8 col-md-8")
    actor_details = left_side.find("div", class_="col-sm-8 col-lg-12 col-md-12")
    biography_text = actor_details.find_all(string=True, recursive=False)
    biography = ''.join(biography_text)

    right_side = soup.find("div", class_="col-lg-4 col-md-4")
    actor_picture = right_side.find('img', class_="img-responsive")

    details = {}
    details_list_items = right_side.find("ul", class_="list m-b-0").find_all("li", class_="list-item p-a-0")
    for list_item in details_list_items:
        dict_items = list_item.text.split(':')
        key = dict_items[0].strip()
        value = dict_items[1].strip()
        details[key] = value
    details['Biography'] = biography
    details['MDL ID'] = mdl_id
    print(details)
    print(f"Picture URL: {actor_picture['src']}")

    return details, actor_picture['src']   # returns a dictionary of scraped actor data and link to actor's picture

# Go through the whole page, scraping all Main and Supporting roles
def scrape_page(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    URL = "https://mydramalist.com"

    left_side = soup.find("div", class_="col-lg-8 col-md-8")
    staff_boxes = left_side.find("div", class_="box-body")
    all_role_headers = staff_boxes.find_all("h3", class_="header b-b p-b")
    all_corresponding_ul = staff_boxes.find_all("ul", class_="list no-border p-b clear")

    # loop through all the headers in cast page (Director, Screenwriter, Main Role, etc)
    for i, role in enumerate(all_role_headers):
        print(f"{i} | {role.text}")
        
        if (role.text.strip() == "Main Role") or (role.text.strip() == "Support Role"):      
            all_actors = all_corresponding_ul[i].find_all("li", class_="list-item col-sm-6") # Get all list items for each actor of this category

            for actor in all_actors:
                character_details = {}
                character_name = actor.find('small').text.strip()
                role = actor.find('small', class_='text-muted').text.strip()
                print(f"Actor name: {actor.find('b').text} | Character name: {character_name} | Role: {role}")
                actor_page_url = URL + actor.find('a').get('href')
                print(f"Actor page url: {actor_page_url}")

                character_details['Character name'] = character_name
                character_details['Role'] = role
                actor_details, actor_picture_URL = scrape_actor(actor_page_url)

                move_to_db(actor_details, character_details, actor_picture_URL)
                print()
                sleep(random.randint(3,5))


def main():
    # actor_link_1 = "https://mydramalist.com/people/1974-jo-jung-suk"
    actor_link_2 = "https://mydramalist.com/people/23666-shim-dal-gi"
    wsup, wsup_URL = scrape_actor(actor_link_2)
    nothing = ""
    move_to_db(wsup, nothing, wsup_URL)
    # page_link = "https://mydramalist.com/25560-moving/cast"
    # scrape_page(page_link)
    # test()


main()