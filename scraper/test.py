import requests
from bs4 import BeautifulSoup

URL = "https://mydramalist.com/25560-moving"

IP_URL = "htt"

moving_page = requests.get(URL)
soup = BeautifulSoup(moving_page.content, "html.parser")

cover_div = soup.find("div", class_="col-sm-4 film-cover cover")
cover_url = cover_div.find("img", class_="img-responsive")['src']
print(cover_url)

with open("scraped_data/penis.jpg", 'wb') as f:
    response = requests.get(cover_url)
    f.write(response.content)

