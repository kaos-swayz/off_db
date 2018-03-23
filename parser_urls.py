from _main import unpack_data_file, fetch_soup, test_connection, save_json_file

from itertools import chain
import os
import requests
import json

import bs4 as bs


class ParserUrls:
    def __init__(self, name_of_set):
        self.name_of_set = name_of_set
        self.url_base_file = "urls/bs4_url_base_datapack_{}.txt".format(self.name_of_set)
        self.url_base = unpack_data_file("urls/bs4_url_base_datapack_{}.txt".format(self.name_of_set))
        self.url_output_file = "urls/st1_urls_set_{}.txt".format(self.name_of_set)
        self.bs4_selectors = unpack_data_file("urls/bs4_selectors_{}.txt".format(self.name_of_set))
        self.bs4_selectors_reff = self.set_bs4_selectors_reff()

    def set_bs4_selectors_reff(self):
        try:
            return unpack_data_file("urls/bs4_selectors_reff_{}.txt".format(self.name_of_set))
        except:
            return None



    """ MAIN FUNCTIONS """

    def get_data(self, output_file_name, func, clear_file=True):
        # main function
        if clear_file == True:
            self.clear_file(file_name=output_file_name)
        else:
            pass

        output = func

        self.add_files_to_output_file(url_list=output, output_file_name=output_file_name)


    def parse_for_urls_by_pages(self, min_page=0, max_page=9999):
        # parse for urls by pages
        output = []

        for page_n in range(min_page, max_page):
            # generate url by joining all parts of url_data list
            url = "".join(self.url_base).format(page_n)
            print("fetching urls from: {}".format(url))

            output_urls = self.fetch_links(fetch_soup(url), bs4_selectors_set=self.bs4_selectors)

            for url in output_urls:
                output.append(url)

        return output



    def parse_for_urls_by_refferences(self, input_data=None, input_file_name=None, max_iterations=99999):
        # get data from a file or list data structure
        # and then parse site using urls from data
        # and append new url found to data
        data = self.specify_input_data_source(input_data=input_data, input_file_name=input_file_name)

        n = 0
        for url in data:

            print("fetching urls from: {} - {}".format(n, url))
            urls = self.fetch_links(fetch_soup(url), bs4_selectors_set=self.bs4_selectors_reff)
            # urls = self.fetch_links(fetch_soup(url), bs4_selectors_set=["a", "class", "card"])
            print("upcoming check for urls: {}".format(urls))

            for new_url in urls:

                new_to_set = self.check_if_url_is_new(new_url, list_of_url_datapacks_to_compare=[data])

                if new_to_set == True:
                    print(" *** new url confirmed: {}".format(new_url))
                    data.append(new_url)

            n += 1
            if n >= max_iterations:
                break

        return data




    def fetch_links(self, soup, bs4_selectors_set):
        self.check_bs4_selectors(bs4_selectors_set)

        output = []

        html_target_element = bs4_selectors_set[0]
        css_id_type = bs4_selectors_set[1]
        css_id_value = bs4_selectors_set[2]
        # print("{}, {}, {}".format(html_target_element, css_id_type, css_id_value))
        #
        # print(soup)

        for link in soup.find_all(html_target_element, {css_id_type: css_id_value}):
            # print("***")
            # print(link)
            try:
                link = link.find("a").get("href")
            except AttributeError as err:
                link = link.get("href")
            if "http" in link:
                url = link
            else:
                url = "".join(self.url_base[0] + link)
            print("{}".format(url))

            output.append(url)

        return output


    """ saving / clearing files """

    def clear_file(self, file_name):
        with open(file_name, "w", encoding="UTF-8") as fp:
            fp.write("")
        print("data cleared from file: {}".format(file_name))


    def add_files_to_output_file(self, url_list, output_file_name):
        for url in url_list:
            with open(output_file_name, "a", encoding="UTF-8") as fp:
                fp.write(url + "\n")
        print("all data appended to: {}".format(output_file_name))



    """ parse_for_urls_by_refferences subfunctions """

    def specify_input_data_source(self, input_data, input_file_name):
        if input_data != None and input_file_name == None:
            data = input_data
        elif input_data == None and input_file_name != None:
            data = unpack_data_file(input_file_name)
        else:
            raise Exception("No clear data source specified")

        return data

    def check_if_url_is_new(self, new_url, list_of_url_datapacks_to_compare):
        # WARNING! REMEMBERT TO PUT list_of_url_datapacks_to_compare PARAMETER IN LIST
        new_to_set = True

        for datapack in list_of_url_datapacks_to_compare:
            self.check_datapack(datapack)
            for url in datapack:
                if new_url in url:
                    new_to_set = False

        return new_to_set

    """ debug """

    def check_bs4_selectors(self, bs4_selectors_set):
        if bs4_selectors_set == None:
            raise Exception("no bs4 selectors set! (note: check bs4_selectors_reff)")

    def check_datapack(self, datapack):
        if type(datapack) != list:
            raise Exception("datapack expected to be list! \n(note: check if you use list as a list_of_url_datapacks_to_compare parameter)")


if __name__ == "__main__":
    p = ParserUrls("rm")

    p.get_data(func=p.parse_for_urls_by_pages(max_page=150), output_file_name="urls/st1_urls_set_rm.txt")
    # p.get_data(func=p.parse_for_urls_by_refferences(input_file_name="urls/st1_urls_set_rm.txt"), output_file_name="urls/st1_urls_set_rm.txt")
