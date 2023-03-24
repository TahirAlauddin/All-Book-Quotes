import requests
from bs4 import BeautifulSoup


def write_data(data):
    with open("links.txt", "a") as file:
        for i in data:
            file.write(i + '\n')


url = "https://bookquoters.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
last_page = soup.find_all("a", class_="item")[-1].text.strip()

links = []
for i in range(1, int(last_page) + 1):
    url = "https://bookquoters.com?page=" + str(i)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        collection_thumb_div = soup.find_all("div", class_="collection_thumb")
        # Do something with the HTML here
    else:
        print("Error retrieving page.")

    for link in collection_thumb_div:
        links.append(link.find("a", class_="ui fluid image")["href"])

write_data(links)
