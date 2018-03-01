from _main import unpack_data_file, fetch_soup, test_connection, save_json_file

import os
import requests
import json

import bs4 as bs


class ParserRawData:
    def __init__(self, urls_input_file):
        self.urls = unpack_data_file(urls_input_file)

        # name_of_set derivative - variables that are made basing on what set we want to parse
        # what is there is no name of set
        self.name_of_set = urls_input_file[urls_input_file.rfind("_") + 1:urls_input_file.find(".")]
        self.url_base = unpack_data_file("urls/url_base_datapack_{}.txt".format(self.name_of_set))
        self.raw_data_output_file = "datasets/raw_data_{}.json".format(self.name_of_set)


    def fetch_element(self, soup, output_list, html_target_element, css_id_type="class", css_css_id_value=None):
        for e in soup.find_all(html_target_element, {css_id_type: css_css_id_value}):
            output_list.append(e.text.replace("\n", ""))

    def fetch_property(self, soup, output_list, html_target_element, property_name, css_id_type=None, css_id_value=None):
        property_value = soup.find(html_target_element, {css_id_type: css_id_value}).get(property_name)
        output_list.append(property_value)



    """ chooses fetcher based on what dataset we are in """

    def fetch_raw_data(self, soup, url):

        if self.name_of_set == "rm":
            return self.fetch_raw_data_rm(soup, url)
        if self.name_of_set == "bj":
            return self.fetch_raw_data_bj(soup,url)



    """ fetchers """

    def fetch_raw_data_rm(self, soup, url):
        print("fetching data from: " + url)

        output = []
        #id
        self.fetch_property(soup, output_list=output, html_target_element="h1", property_name="data-id")
        #name
        self.fetch_element(soup, output_list=output, html_target_element="h1", css_css_id_value="h3")
        #source
        output.append(url[url.find("www")+4:url.find(".",url.find("www")+5)])
        #url
        output.append(url)
        #img url
        temp_list = []
        try:
            self.fetch_property(soup, output_list=temp_list, html_target_element="div", property_name="data-bg", css_id_type="class",
                       css_id_value="rmb-object-slide")
            output.append(self.url_base[0] + temp_list[0])
        except AttributeError as err:
            print("An error: {} have occured on url: {}".format(err, url))
            output.append("")
        #all data
        self.fetch_element(soup, output_list=output, html_target_element="div", css_css_id_value="rmb-details-list-item")
        #disabled fit-out elements
        fitout_disabled = []
        self.fetch_element(soup, output_list=fitout_disabled, html_target_element="span", css_css_id_value="rmb-details-list-disabled")
        output.append(fitout_disabled)
        # empty string for debuging reasons
        output.append("")

        return output

    def fetch_raw_data_bj(self, soup, url):
        print("fetching data from: " + url)

        if self.try_if_not_404(soup, url) == True:

            output = []

            # id
            output.append(url[28:url.find(".html")])
            # name
            self.fetch_element(soup, output_list=output, html_target_element="h1")
            # source
            output.append(url[url.find("www") + 4:url.find(".", url.find("www") + 5)])
            # url
            output.append(url)
            # img url
            temp_list = []
            try:
                element = soup.find("div", {"class": "building-carousel"})
                self.fetch_property(element, output_list=temp_list, html_target_element="img", property_name="src")
                output.append(temp_list[0])
            except AttributeError as err:
                print("An error: {} have occured on url: {}".format(err, url))
                output.append("")
            # address
            self.fetch_element(soup, output_list=output, html_target_element="p", css_css_id_value="location")
            # all data
            # print("Building completely leased" in [e.text for e in soup.find_all("p")])
            bj_offer_sec = ["Available space", "Availability", "Asking rent", "Rent for parking", "Minimum office unit",
                            "Minimum lease term", "Service charge"]
            for e in [e.text for e in soup.find_all("p")]:
                if e == "Building completely leased.":
                    for e in bj_offer_sec:
                        output.append(e + "Leased")
            element = soup.find("section", {"class": "building-details"})
            self.fetch_element(element, output_list=output, html_target_element="li")
            # #disabled fit-out elements
            # fitout_disabled = []
            # fetch_element(soup, output_list=fitout_disabled, html_target_element="span", css_css_id_value="rmb-details-list-disabled")
            # output.append(fitout_disabled)
            # empty string for debuging reasons
            output.append("")


            # print(output)
            return output

    """ final parser function """

    def parse_by_links(self, urls, output_file_name, max_iterations=9999):
        # parses through all elements
        output = []
        n = 0
        for e in urls:
            e = self.bug_fixer(url=e, set=self.name_of_set)
            output.append(self.fetch_raw_data(fetch_soup(e), url=e))
            n += 1
            if n == max_iterations:
                break
        save_json_file(file_name=output_file_name, content=output)

    def bug_fixer(self, url, set):
        if set == "rm":
            pass
        elif set == "bj":
            url = url.replace("é", "e")
            url = url.replace("https://www.officefinder.pl/office-warsaw-lewartowskiego-6.html", "https://www.officefinder.pl/office-warsaw-edelmana-6-dawniej-lewartowskiego-6.html")
        return url

    def try_if_not_404(self, soup, url):
        if "error 404" in soup.title.text.lower():
            return False
        else:
            return True


if __name__ == "__main__":
    p = ParserRawData(urls_input_file="urls/urls_output_bj.txt")
    p.parse_by_links(urls=p.urls, output_file_name=p.raw_data_output_file)
    # p.fetch_raw_data_bj(fetch_soup("https://www.officefinder.pl/office-katowice-centrum-biurowe-francuska-a-sublease-2155.html"), "https://www.officefinder.pl/office-katowice-centrum-biurowe-francuska-a-sublease-2155.html")