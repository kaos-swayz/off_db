from _main import unpack_data_file, fetch_soup, test_connection, save_json_file

import os
import requests
import json

import bs4 as bs


class ParserUrls:
    def __init__(self, url_base_file):
        self.url_base = unpack_data_file(url_base_file)

        # name_of_set derivative - variables that are made basing on what set we want to parse
        # what is there is no name of set
        self.name_of_set = url_base_file[url_base_file.rfind("_") + 1:url_base_file.find(".")]
        self.url_output_file = "urls/urls_output_{}.txt".format(self.name_of_set)
        self.bs4_selectors = unpack_data_file("urls/bs4_selectors_{}.txt".format(self.name_of_set))




    def fetch_links(self, soup, bs4_selectors_set, output_file_name):
        html_target_element = bs4_selectors_set[0]
        css_id_type = bs4_selectors_set[1]
        css_id_value = bs4_selectors_set[2]

        for link in soup.find_all(html_target_element, {css_id_type: css_id_value}):
            try:
                link = link.find("a").get("href")
            except AttributeError as err:
                link = link.get("href")
            if "http" in link:
                url = link
            else:
                url = "".join(self.url_base[0] + link)
            print(url)
            with open(output_file_name, "a", encoding="UTF-8") as fp:
                fp.write(url + "\n")


    def parse_by_pages(self, min_page=0, max_page=9999, clear_file=True):
        if clear_file == True:
            with open(self.url_output_file, "w", encoding="UTF-8") as fp:
                fp.write("")
        else:
            pass

        for page_n in range(min_page, max_page):
            # generate url by joining all parts of url_data list
            url = "".join(self.url_base).format(page_n)
            print("fetching urls from: {}".format(url))
            self.fetch_links(fetch_soup(url), bs4_selectors_set=self.bs4_selectors, output_file_name=self.url_output_file)




if __name__ == "__main__":
    p = ParserUrls("urls/url_base_datapack_rm.txt")

    # p.fetch_links(soup, bs4_selectors_set=p.bs4_selectors, output_file_name=p.url_output_file)
    p.parse_by_pages(min_page=1, max_page=96)