from _main import unpack_url_data, fetch_soup, test_connection

import requests

import bs4 as bs

def fetch_links(soup, output_file_name="urls_output.txt"):
    for link in soup.find_all("a", {"class": "rmb-object-list-item"}):
        url = "".join(url_data[0] + link.get("href"))
        print(url)
        with open(output_file_name, "a", encoding="UTF-8") as fp:
            fp.write(url + "\n")

def parse_by_pages(url_data, min_page=0, max_page=9999):
    for i in range(min_page, max_page):
        # code generates url by joining all parts of url_data list
        url = "".join(url_data) + str(i)
        fetch_links(fetch_soup(url),output_urls)





if __name__ == "__main__":
    input_file_name = "url_data_set1.txt"
    output_urls = "urls_output_set1.txt"

    url_data = unpack_url_data(input_file_name)

    parse_by_pages(url_data, min_page=0, max_page=94)