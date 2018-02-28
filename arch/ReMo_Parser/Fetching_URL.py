#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

miasta_src = """<select name="city[]" id="city" multiple="multiple">
                          <option value="922410">Białystok</option>
                          <option value="928363">Bydgoszcz</option>
                          <option value="938670">Bytom</option>
                          <option value="938887">Chorzów</option>
                          <option value="930868">Częstochowa</option>
                          <option value="932703">Elbląg</option>
                          <option value="933016">Gdańsk</option>
                          <option value="934100">Gdynia</option>
                          <option value="940000">Gliwice</option>
                          <option value="970632">Gniezno</option>
                          <option value="937474">Katowice</option>
                          <option value="945930">Kielce</option>
                          <option value="950463">Kraków</option>
                          <option value="954047">Legnica</option>
                          <option value="954700">Lublin</option>
                          <option value="964465">Olsztyn</option>
                          <option value="965016">Opole</option>
                          <option value="969400">Poznań</option>
                          <option value="972750">Radom</option>
                          <option value="974133">Rzeszów</option>
                          <option value="934783">Sopot</option>
                          <option value="943428">Sosnowiec</option>
                          <option value="977976">Szczecin</option>
                          <option value="982724">Toruń</option>
                          <option value="918123">Warszawa</option>
                          <option value="986283">Wrocław</option>
                          <option value="957650">Łódź</option>
                        </select>"""

miasta = ["chorzow", "poznan"]
miasta2 = ["warszawa", "szczecin", "gdansk", "sopot", "gdynia", "olsztyn", "bydgoszcz", "torun", "wroclaw", "lodz",
          "wroclaw", "krakow", "katowice", "lublin", "poznan", "rzeszow", "bialystok", "chorzow", "gliwice"]


base_url = "http://www.remobile.pl/pl/biura/"

src_urls = {}
sw = " === "

building_urls = []

def fetch_html(src_url):
    #function takes url and returns pure html
    print(sw + "fetching html from " + src_url + sw)
    r = urllib2.urlopen(src_url)
    html = r.read()
    return html

def r_rest(html,extr):
    #find the extraction spot and return rest of string
    stop_no = html.find(extr) + 1
    rest_html = html[stop_no:]
    return rest_html

"""
def url_compliter(url, src_url):
    src_url = r_rest(r_rest(src_url, "/"),"/")
    base_url = src_url[:src_url.find("/")]
    return base_url + url
"""

def extr_building_urls(html, extr_point):
    #functon takes pure html, finds the correct spot and finds corrects urls starting from it
    rest_html = r_rest(r_rest(r_rest(html, extr_point), "a href"), '"')
    ex_stop_no = rest_html.find('"')
    ex_url = rest_html[0: ex_stop_no]
    building_urls.append("http://www.remobile.pl" + ex_url)
    return rest_html

def ext_loop(html, extr_point):
    n = 0
    #n variable used for security reasons
    while extr_point in html:
        html = extr_building_urls(html, extr_point)
        n = n + 1
        if n == 50:
            break
    return html


def pagination(html, e):
    #when extraction is completed finds next page src_url and adds it to src_urls
    if '"next_page_button">' in html:
        rest_html = r_rest(r_rest(r_rest(html, '"next_page_button">'), "href"), '"')
        ex_stop_no = rest_html.find('"')
        ex_url = rest_html[0: ex_stop_no]
        src_urls[e].append("http://www.remobile.pl" + ex_url)
        #all_src_urls.append("http://www.remobile.pl" + ex_url)
    else:
        return None

def write_to_file(e):
    #takes building_urls list and writes it to specific file
    file = open(e + ".txt","w")
    for item in building_urls:
        file.write("%s\n" % item)
    file.close()

def fetch_b_urls(src_url, e):
    #takes a list of src_urls, gets pure html, loops for building_urls, then changes page and adds page to src_urls
    #n variable used for security reasons
    n = 1
    while len(src_url) > 0:
        src = src_url.pop()
        html = fetch_html(src)
        html = ext_loop(html, "<h3>")
        pagination(html, e)
        n = n + 1
        if n == 50:
            break

def parse(list, dict):
    for e in list:
        building_urls = []
        url_list = dict.get(e)
        fetch_b_urls(url_list, e)
    write_to_file("all_b_urls")


def complete_url_list(input_list, base_url, output_dict):
    for e in input_list:
        r = []
        f_url = base_url + e + "/"
        r.append(f_url)
        output_dict[e] = r

complete_url_list(miasta, base_url, src_urls)
print(src_urls)
parse(miasta, src_urls)

#do poprawy - building_urls zbiera się do jednej listy i przez to wszystko jest w jednym pliku
#global albo init mógłby to naprawić