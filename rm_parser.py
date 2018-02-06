from _main import unpack_url_data, fetch_soup, test_connection

import requests
import json

import bs4 as bs



def fetch_links(soup, output_file_name="urls_output.txt"):
    for link in soup.find_all("a", {"class": "rmb-object-list-item"}):
        url = "".join(url_base[0] + link.get("href"))
        # print(url)
        with open(output_file_name, "a", encoding="UTF-8") as fp:
            fp.write(url + "\n")

def parse_by_pages(url_data_list, min_page=0, max_page=9999, output_url_list="urls_output"):
    for i in range(min_page, max_page):
        # code generates url by joining all parts of url_data list
        url = "".join(url_data_list) + str(i)
        print("fetching urls from: {}".format(url))
        fetch_links(fetch_soup(url),output_url_list)



def fetch_element(soup, output_list, el_name, css_class_name):
    for e in soup.find_all(el_name, {"class": css_class_name}):
        output_list.append(e.text.replace("\n", ""))

def fetch_property(soup, output_list, el_name, property_name, id_name=None, id_value=None):
    property_value = soup.find(el_name, {id_name: id_value}).get(property_name)
    output_list.append(property_value)

def fetch_all_raw_data(soup, url):
    print("fetching data from: " + url)

    output = []

    #id
    fetch_property(soup, output_list=output, el_name="h1", property_name="data-id")
    #name
    fetch_element(soup, output_list=output, el_name="h1", css_class_name="h3")
    #url
    output.append(url)
    #img url
    temp_list = []
    try:
        fetch_property(soup, output_list=temp_list, el_name="div", property_name="data-bg", id_name="class",
                   id_value="rmb-object-slide")
        output.append(url_base[0] + temp_list[0])
    except AttributeError as err:
        print("An error: {} have occured on url: {}".format(err, url))
        output.append(temp_list)
    #all data
    fetch_element(soup, output_list=output, el_name="div", css_class_name="rmb-details-list-item")
    #disabled fit-out elements
    fitout_disabled = []
    fetch_element(soup, output_list=fitout_disabled, el_name="span", css_class_name="rmb-details-list-disabled")
    output.append(fitout_disabled)
    # empty string for debuging reasons
    empty_string = ""
    output.append(empty_string)

    return output

def parse_by_links(url_data_list, output_file_name="raw_data.txt"):
    output = []
    # n = 0
    for e in url_data_list:
        output.append(fetch_all_raw_data(fetch_soup(e), url=e))
        # n += 1
        # if n == :
        #     break
    with open(output_file_name, "w") as f:
        f.write(json.dumps(output))





if __name__ == "__main__":
    input_file_name = "url_data_set1.txt"
    output_urls = "urls_output_set1.txt"
    output_raw_data = "raw_data_set1.txt"

    url_base = unpack_url_data(input_file_name)
    # parse_by_pages(url_base, min_page=0, max_page=94, output_url_list=output_urls)


    urls = unpack_url_data(output_urls)
    parse_by_links(urls, output_file_name=output_raw_data)
    # soup = fetch_soup("http://www.remobile.pl/pl/biura/krakow/big,2217#3a4bc864")
    # fetch_all_raw_data(soup)

