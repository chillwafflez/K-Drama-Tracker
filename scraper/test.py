import requests
from bs4 import BeautifulSoup

URL = "https://mydramalist.com"
first_page_sk_dramas_URL = URL + "/search?adv=titles&ty=68&co=3&so=top"

IP_URL = "htt"

top_KDs_1st_page = requests.get(first_page_sk_dramas_URL)
soup = BeautifulSoup(top_KDs_1st_page.content, "html.parser")

