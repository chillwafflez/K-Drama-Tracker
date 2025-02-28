import requests
from bs4 import BeautifulSoup
from time import sleep
import random

URL = "https://mydramalist.com"
# top_kdramas_link = URL + "/search?adv=titles&ty=68&co=3&so=top"
top_kdramas_link = URL + "/search?adv=titles&ty=68&co=3&st=3&so=top"
output_file_name = "data/completed_SK_links.txt"
output_file = open(output_file_name, "w", encoding="utf-8") 

# Loop through each page, saving links to each completed South Korean drama to text file
for i in range(1,3):    # currently 179 pages
    # Get page
    print(f"-----PAGE {i}-----")
    page_link = top_kdramas_link + "&page=" + str(i)
    page = requests.get(page_link)
    soup = BeautifulSoup(page.content, "html.parser")

    # HTML container for all the dramas on the page
    drama_container = soup.find("div", class_="col-lg-8 col-md-8")
    all_drama_divs = drama_container.find_all("div", class_ = "box")
    for drama in all_drama_divs:
        drama_id = drama['id'].split("-")[1]                                # Drama's ID in their records
        text_primary_title = drama.find("h6", class_="text-primary title")
        drama_title = text_primary_title.find("a").text                     # Drama's title
        drama_link = text_primary_title.find("a").get('href')               # Drama's link
        print(f"NAME: {drama_title} | ID: {drama_id} | LINK: {URL + drama_link}")
        output_file.write(URL + drama_link + "\n")
    sleep(random.randint(5,15))

output_file.close()
