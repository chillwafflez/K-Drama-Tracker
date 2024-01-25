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

    # --- Get extra info (div under show_detailsxx and right below show-synopsis) --- #
    extra_info = left_side.find("ul", class_="list m-a-0")

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
    else:
        print("NO RELATED CONTENT")

    # Save drama's related content if there is any
    if related_content_exists:
        with open("./data/completed_SK_related.csv", mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([title, year, mdl_id, prequel_str, compilation_str, sequel_str, spinoff_str])

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

def main():
    # # test_link = "https://mydramalist.com/710963-yeonhwa-palace"
    # # test_link = "https://mydramalist.com/57173-hospital-playlist-2" # multiple related content (compilation)
    try:
        test_link = "https://mydramalist.com/9025-nirvana-in-fire"
        # test_link = "https://mydramalist.com/57173-hospital-playlist-2" # multiple related content (compilation)
        # test_link = "https://mydramalist.com/702267-weak-hero"
        # test_link = "https://mydramalist.com/36269-doctor-playbook"
        scrape_page_completedSK(test_link)
    except Exception:
        print("Error encountered. Not entering into db")

main()