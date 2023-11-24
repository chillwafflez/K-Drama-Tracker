import requests
from bs4 import BeautifulSoup

URL = "https://mydramalist.com"
first_page_sk_dramas_URL = URL + "/search?adv=titles&ty=68&co=3&so=top"

top_KDs_1st_page = requests.get(first_page_sk_dramas_URL)
soup = BeautifulSoup(top_KDs_1st_page.content, "html.parser")

j = 0
curr_page_drama_links = []
while j < 3:
    # --Getting all links for K-Dramas from Top Dramas page 1--
    drama_container = soup.find("div", class_="col-lg-8 col-md-8")
    all_drama_divs = drama_container.find_all("div", class_ = "box")
    for drama in all_drama_divs:
        drama_title_h6 = drama.find("h6", class_="text-primary title")
        drama_link = drama_title_h6.find("a").get('href')
        print(f"Link: {URL + drama_link}")
        curr_page_drama_links.append(URL + drama_link)
    j += 1
    
print(f"Links to each drama on current page: {curr_page_drama_links}")


    # # Go through each link to get info on each drama
    # for i in range(0, 2):
    #     current_page = requests.get(curr_page_drama_links[i])
    #     # Parsing the HTML
    #     drama_soup = BeautifulSoup(current_page.content, "html.parser")

    #     entire_drama_box = drama_soup.find("div", class_="col-lg-8 col-md-8 col-rightx")
    #     entire_drama_box = entire_drama_box.find("div", class_="box")

    #     # Get Synopsis
    #     drama_synopsis = entire_drama_box.find("div", class_="show-synopsis").find("span").text
    #     drama_synopsis = drama_synopsis.split("(")[0]
    #     print("Synopsis: ")

    #     # Get Rating
    #     drama_rating = entire_drama_box.find("div", class_="box deep-orange").text

    # Go to next page
    # next_page = drama_container.find("li", )
    # soup = 
    # print(curr_page_drama_links)
    # j = 3


        