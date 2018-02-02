import requests

import bs4 as bs


def unpack_url_data(file_name):
    with open(file_name, "r", encoding="UTF-8") as fp:
        url_data = fp.read()
    # print(url_data)
    return url_data

def fetch_soup(url):
    session = requests.Session()
    response = session.get(url)
    html = response.content
    soup = bs.BeautifulSoup(html, "lxml")
    return soup



def test_connection(soup):
    print(soup.title)
    print(soup.title.name)
    print(soup.title.string)

if __name__ == "__main__":
    soup = fetch_soup(unpack_url_data("url_data.txt"))

    test_connection(soup)