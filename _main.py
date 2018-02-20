import requests
import json

import bs4 as bs



def unpack_url_data(file_name):
    """ pattern = url_data[0] - base url, url_data[1] - ext url """
    with open(file_name, "r", encoding="UTF8") as fp:
        url_data = fp.read().split()
    # print(url_data)
    return url_data

def fetch_soup(url):
    session = requests.Session()
    response = session.get(url)
    html = response.content
    soup = bs.BeautifulSoup(html, "lxml")
    return soup



def save_json_file(file_name, content):
    with open(file_name, "w", encoding="UTF8") as f:
        f.write(json.dumps(content))
    print("saved to a file: {}".format(file_name))

def open_json_file(file_name):
    with open(file_name, "r", encoding="UTF8") as fp:
        data = json.loads(fp.read())
    return data


def test_connection(soup):
    print(soup.title)
    print(soup.title.name)
    print(soup.title.string)

if __name__ == "__main__":
    input_file_name = "url_data.txt"
    output_urls = "urls_output.txt"

    url = "".join(unpack_url_data(input_file_name))
    soup = fetch_soup(url)

    test_connection(soup)