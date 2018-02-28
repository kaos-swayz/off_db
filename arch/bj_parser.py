from _main import unpack_url_data, fetch_soup, test_connection, save_json_file

import requests
import json

import bs4 as bs


def fetch_links(soup, output_file_name="urls_output.txt"):
    for link in soup.find_all("div", {"class": "building-list__item"}):
        url = "".join(url_base[0] + link.find("a").get("href"))
        print(url)
        with open(output_file_name, "a", encoding="UTF-8") as fp:
            fp.write(url + "\n")


def parse_by_pages(url_data_list, min_page=0, max_page=9999, output_url_list="urls_output"):
    for i in range(min_page, max_page):
        # code generates url by joining all parts of url_data list
        url = "".join(url_data_list).format(str(i))
        print("fetching urls from: {}".format(url))
        fetch_links(fetch_soup(url),output_url_list)




def fetch_element(soup, output_list, el_name, css_class_name=None):
    for e in soup.find_all(el_name, {"class": css_class_name}):
        output_list.append(e.text.replace("\n", ""))

def fetch_property(soup, output_list, el_name, property_name, id_name=None, id_value=None):
    property_value = soup.find(el_name, {id_name: id_value}).get(property_name)
    output_list.append(property_value)

def fetch_all_raw_data(soup, url):
    print("fetching data from: " + url)

    output = []

    try:
        #id
        output.append(url[28:url.find(".html")])
        #name
        fetch_element(soup, output_list=output, el_name="h1")
        #url
        output.append(url)
        #img url
        temp_list = []
        try:
            element = soup.find("div", {"class":"building-carousel"})
            fetch_property(element, output_list=temp_list, el_name="img", property_name="src")
            output.append(temp_list[0])
        except AttributeError as err:
            print("An error: {} have occured on url: {}".format(err, url))
            output.append(temp_list)
        #address
        fetch_element(soup, output_list=output, el_name="p", css_class_name="location")
        #all data
        # print("Building completely leased" in [e.text for e in soup.find_all("p")])
        bj_offer_sec = ["Available space", "Availability", "Asking rent", "Rent for parking", "Minimum office unit", "Minimum lease term", "Service charge"]
        for e in [e.text for e in soup.find_all("p")]:
            if e == "Building completely leased.":
                for e in bj_offer_sec:
                    output.append(e + "Leased")
        element = soup.find("section", {"class":"building-details"})
        fetch_element(element, output_list=output, el_name="li")
        # #disabled fit-out elements
        # fitout_disabled = []
        # fetch_element(soup, output_list=fitout_disabled, el_name="span", css_class_name="rmb-details-list-disabled")
        # output.append(fitout_disabled)
        # empty string for debuging reasons
        empty_string = ""
        output.append(empty_string)
    except:
        print("error while fetching")


    print(output)
    return output

def parse_by_links(url_data_list, output_file_name="raw_data.txt"):
    output = []
    # n = 0
    for e in url_data_list:
        output.append(fetch_all_raw_data(fetch_soup(e), url=e))
        # n += 1
        # if n == 10:
        #     break
    save_json_file(file_name=output_file_name, content=output)




if __name__ == "__main__":
    input_file_name = "url_data_set2.txt"
    output_urls = "urls_output_set2.txt"
    output_raw_data = "raw_data_set2.txt"

    url_base = unpack_url_data(input_file_name)
    # parse_by_pages(url_base, min_page=0, max_page=70, output_url_list=output_urls)


    # urls = unpack_url_data(output_urls)
    # parse_by_links(urls, output_file_name=output_raw_data)
    soup = fetch_soup("https://www.officefinder.pl/office-warsaw-dominanta-praska.html")
    raw_data = []
    raw_data.append(fetch_all_raw_data(soup, "https://www.officefinder.pl/office-warsaw-dominanta-praska.html"))
    save_json_file(file_name="raw_data_set_dominanta.json", content=raw_data)
