#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import urllib2
import json
import re

from BasicFunc import r_rest
from BasicFunc import fetch_html
from BasicFunc import phrase_count
from BasicFunc import extract_value
from BasicFunc import leave_digits
from BasicFunc import get_float
from BasicFunc import get_currency

b_data = []
error_urls = []


def read_line(filename):
    #takes a file with urls
    #returns a list of urls
    file_path = path.relpath("miasta_b_urls/" + filename + ".txt")
    with open(file_path) as f:
        lines = f.read()
        return lines.split("\n")

def nesting_dict(name, dict):
    #osadza budynkowy dict w słowniku ogólnym
    b_data[name] = dict

def finding_name(html, dict):
    #znajduje nazwę budynku i wstawia go w pole "name"
    rest_html = r_rest(r_rest(html, "<h1>"), ">")
    ex_stop_no = rest_html.find('<')
    dict["1 name"] = rest_html[0: ex_stop_no]

def finding_location(html, dict):
    #znajduje informacje o lokalizacji i zapisuje je dict["2 location"]
    dict["2 location"] = {}
    rest_html = r_rest(r_rest(r_rest(r_rest(html, '<td class="location_column'), ">"), '<div'), "\n")
    ex_stop_no = rest_html.find('\n')
    temp_location = rest_html[0: ex_stop_no]
    if "," in temp_location:
        stop = temp_location.find(",")
        #print stop
        dict["2 location"]["city"] = temp_location[0: stop].replace(" ", "")
        stop = stop + 2
        dict["2 location"]["district"] = temp_location[stop:]
    else:
        dict["2 location"]["city"] = temp_location[0:].replace(" ", "")
        dict["2 location"]["district"] = ""
    rest_html = r_rest(r_rest(rest_html, '<div'), "\n")
    ex_stop_no = rest_html.find('\n')
    dict["2 location"]["address"] = rest_html[24:ex_stop_no]

def finding_terms(html, dict):
    #znajduje informacje o warunkach najmu i zapisuje jest do dict["4 terms"]
    dict["4 terms"] = {}
    html = r_rest(html, "Wyjściowe warunki najmu")
    for e in terms_pattern:
        fetching_terms(html, dict["4 terms"], e)

def fetching_terms(html, dict, extr, *currency):
    #if currency is True you have to add currency key to dict
    rest_html = r_rest(html, "Wyjściowe warunki najmu")
    rest_html = r_rest(r_rest(r_rest(rest_html, extr), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    value = rest_html[0: ex_stop_no]
    dict[terms_pattern_dict[extr]] = get_float(value)
    #if currency == True:
    dict[terms_pattern_dict[extr] + " currency"] = get_currency(value)

terms_pattern = ["Czynsz", \
                 "pow. handlow", \
                 "Koszty eksploatacyjne</", \
                 "parkingu naziemnego</", \
                 "parkingu podziemnego</"]

terms_pattern_dict = {"Czynsz" : "rent", \
                      "pow. handlow" : "retail rent", \
                      "Koszty eksploatacyjne</" : "service charge", \
                     "parkingu naziemnego</" : "parking onground", \
                     "parkingu podziemnego</" : "parking underground", \
                      "Współczynnik miejsc parkingowych" : "parking ratio"}

def finding_status(html, dict):
    #znajduje informacje o statusie budynku i zapisuje je do dict["3 building info"]
    dict["3 building info"] = {}
    for e in info_pattern:
        fetching_info(html, dict["3 building info"], e)
    fetching_description(html, dict["3 building info"])

def fetching_info(html, dict, extr):
    rest_html = r_rest(r_rest(r_rest(html, extr), 'class="table_field_value'), ">")
    ex_stop_no = rest_html.find('<')
    dict[info_pattern_dict[extr]] = rest_html[0: ex_stop_no]

info_pattern = ["Status budynku</", \
                "wita pow. biurowa netto</", \
                "Data zakończenia budowy</", \
                "pięter naziemnych</", \
                "pięter podziemnych</", \
                "Powierzchnia typowego piętra</", \
                "miejsc parkingowych naziemnych</", \
                "miejsc parkingowych podziemnych</", \
                "Minimalny okres najmu</", \
                "Współczynnik pow. wspólnych</", \
                "Współczynnik miejsc parkingowych"]

info_pattern_dict = {"Status budynku</" : "status", \
                "wita pow. biurowa netto</" : "total space", \
                "Data zakończenia budowy</" : "completion date", \
                "pięter naziemnych</" : "no of floors onground", \
                "pięter podziemnych</" : "no of floors underground", \
                "Powierzchnia typowego piętra</" : "floor plate", \
                "miejsc parkingowych naziemnych</" : "no of parking places onground", \
                "miejsc parkingowych podziemnych</" : "no of parking places underground", \
                "Minimalny okres najmu</" : "min lease term", \
                "Współczynnik pow. wspólnych</" : "add-on factor", \
                "Współczynnik miejsc parkingowych" : "parking ratio"}

def fetching_description(html, dict):
    #znajduje opis i wstawia go w pole "description'
    rest_html = r_rest(r_rest(html, '<div id="description"'), "\n")
    ex_stop_no = rest_html.find('<')
    dict["description"] = rest_html[20: ex_stop_no]

def stardard_status_test(s):
    #sprawdza czy elements standardu jest czy go nie ma
    if "inactive_table_field" in s:
        return False
    else:
        return True

def finding_standard(html, dict):
    #wyciąga elementy standardu, sprawdza czy są czy ich nie ma i zapisuje je do dict["5 building standard"]
    dict["5 building standard"] = {}
    rest_html = r_rest(html, "Standard wykończeń</")
    table_of_standard = rest_html[0:rest_html.find("</tbody>")]
    n = 0
    while n < 16:
        rest_html = r_rest(rest_html, 'table_field_label')
        ex_stop_no = rest_html.find('</td')
        temp_location = rest_html[0: ex_stop_no]
        temp_location2 = r_rest(r_rest(temp_location, "span"), ">")
        field_name = temp_location2[0:temp_location2.find("<")]
        dict["5 building standard"][field_name] = stardard_status_test(temp_location)
        n += 1


#=== finding av spaces ===

def finding_offices(html,dict):
    dict["6 rentable area"] = {}
    unclear_tables = []
    rest_html = html
    for e in range(phrase_count(rest_html, '<table class="building_space_table')):
        unclear_tables.append(preparing_table(rest_html))
        rest_html = r_rest(r_rest(r_rest(rest_html, '<table class="building_space_table'), '</table>'), ">")
    clear_tables = []
    #for e in unclear_tables:
    #    print e
    for e in unclear_tables:
        if checking_multibuildings(e) == True:
            clear_tables.append(e)
        else:
            d_table = deconstructing_table(e)
            #print d_table
            for table in range(phrase_count(d_table, '<table class="building_space_table')):
                clear_tables.append(d_table[0:(d_table.find(">", d_table.find('</table>'))) + 1])
                d_table = r_rest(r_rest(r_rest(d_table, '<table class="building_space_table'), '</table>'), ">")
    no = 1
    for e in clear_tables:
        #print "element " + str(no)
        #print e
        fetching_offices(e, dict["6 rentable area"], no)
        no += 1

fl_pattern = ['td class="total_space', \
              'td class="available_space', \
              'space_description', \
              'class="available_from']

fl_pattern_dict = {'td class="total_space' : "nla", \
              'td class="available_space' : "total av space", \
              'space_description' : "av space descr", \
              'class="available_from' : "since when"}

def fetching_offices(html, dict, no):
    #nazwa budynku
    b_no = "b no " + str(no)
    dict[b_no] = {}
    dict[b_no]["b name"] = extract_value(html, '<th class="building_header_label')
    #wynajmowalna powierzchnia
    dict[b_no]["b rentable area"] = {}
    #print phrase_count(html, 'class="floor_no')
    for e in range(phrase_count(html, 'class="floor_no')):
        floor_no = "floor " + str(extract_value(html, 'class="floor_no'))
        dict[b_no]["b rentable area"][floor_no] = {}
        fetching_floor(html, dict[b_no]["b rentable area"][floor_no])
        html = r_rest(html, '</tr>')

def fetching_floor(html, dict):
    for e in fl_pattern:
        value = extract_value(html, e)
        if not re.search(r"[a-zA-Z]", value):
            dict[fl_pattern_dict[e]] = leave_digits(value)
        else:
            dict[fl_pattern_dict[e]] = value

def checking_multibuildings(html):
    if phrase_count(html, 'class="building_header_label"') == 1:
        return True
    else:
        return False

#=== preparing table === (done)

def preparing_table(html):
    pure_table = extracting_table(html)
    table_parts = []
    header = getting_headers(pure_table)
    table_parts.append(header)
    for n in range(phrase_count(pure_table, '<td class="floor_no')):
        floor = getting_floors(pure_table)
        table_parts.append(floor)
        pure_table = r_rest(r_rest(pure_table, '<td class="floor_no'), "</tr")
    return "\n".join(table_parts)

def getting_headers(html):
    header_start = html.find('<th class="building_header')
    header_stop = html.find('</tr', header_start)
    header = html[header_start:header_stop]
    return header

def getting_floors(html):
    floor_start = html.find('<td class="floor_no')
    floor_stop = html.find('</tr', floor_start)
    floor = html[floor_start:floor_stop + 5]
    return floor

def extracting_table(html):
    #wyciąga html z samą tabelą
    table_start = html.find('<table class="building_space_table"')
    rest_html = html[table_start:html.find("</table>", table_start)]
    return rest_html

#=== decondstructing and reconstructing === (done)

def setting_separators(html):
    html = html.replace('<td class="combine_minus_value"></td>', "$")
    html = html.replace('</tr>', "$</tr>")
    html = html + "$"
    return html

def deconstructing_table(html):
    pure_table = setting_separators(html)
    pure_table_head = pure_table
    #print pure_table
    head_tables = []
    for n in range(phrase_count(html, '<th class="building_header')):
        #head_table = []
        header = dec_header(pure_table_head)
        head_tables.append(header)
        #head_tables.append(head_table)
        pure_table_head = r_rest(r_rest(pure_table_head, '<th class="building_header'), "</th")
    floor_table = []
    pure_table_floors = pure_table
    for n in range(phrase_count(html, '<td class="floor_no')):
        floor = dec_floor(pure_table_floors)
        floor_table.append(floor)
        pure_table_floors = r_rest(r_rest(pure_table_floors, '<td class="floor_no'), "</tr")
    spaces_tables = []
    pure_table_spaces = pure_table.replace('<td class="floor_no', "")
    #print pure_table_spaces
    while pure_table_spaces.find('<td') > 0:
        #if pure_table_spaces.find('<td class="floor_no') < pure_table_spaces.find('<td', pure_table_spaces.find('class="floor_no')):
            #pure_table_spaces = r_rest(r_rest(r_rest(pure_table_spaces, '<td class="floor_no'), "</td"), ">")
        space = dec_spaces(pure_table_spaces)
        spaces_tables.append(space)
        pure_table_spaces = r_rest(pure_table_spaces, "$")
        #print pure_table_spaces
    #print head_tables
    #print floor_table
    #print len(spaces_tables)
    #for e in spaces_tables:
        #print "element"
        #print e
    return reconstructing_table(head_tables, floor_table, spaces_tables)

def reconstructing_table(list1, list2, list3):
    all_tables = []
    for e in list1:
        temp_table = []
        temp_table.append('<table class="building_space_table">\n')
        all_tables.append(temp_table)
    n = 0
    for e in all_tables:
        e.append(list1[n])
        n += 1
    n = 0
    for e in list2:
        for list in all_tables:
            if '<td class="total_space_value space_body' in list3[n]:
                list.append(e)
                list.append(list3[n])
                list.append('</tr>')
            else:
                pass
            n += 1
    for e in all_tables:
        e.append('</table>')
    new_tables = []
    for e in all_tables:
        for s in e:
            new_tables.append(s)
    #for e in new_tables:
    #    print e
    new_table = "\n".join(new_tables)
    #print new_table
    return new_table

def dec_header(html):
    header_start = html.find('<th class="building_header')
    header_stop = html.find('</th', header_start)
    header = html[header_start:header_stop + 5]
    #stop_point = header_stop + 5
    return header

def dec_floor(html):
    floor_start = html.find('<td class="floor_no')
    floor_stop = html.find('</td', floor_start)
    floor = html[floor_start:floor_stop + 5]
    #stop_point = floor_stop + 5
    return floor

def dec_spaces(html):
    floor_start = html.find('<td')
    floor_stop = html.find('$', floor_start)
    floor = html[floor_start:floor_stop + 1]
    #stop_point = floor_stop + 5
    return floor

"""
data = {}
#z = deconstructing_table(y)
#print z
finding_offices(y, data)
print data

"""

urls = read_line("test")

for e in urls:
    try:
        html = fetch_html(e)
        html = r_rest(html, '<div id="offer_container">')

    except Exception as err:
        print "An error occurred: " + str(err)
        print "Could not fetch: " + str(e)
        error_urls.append(e)
        pass
    data = {}
    finding_name(html, data)
    finding_location(html, data)
    finding_terms(html, data)
    finding_status(html, data)
    finding_standard(html, data)
    finding_offices(html, data)
    b_data.append(data)

#print b_data

with open('result.json', 'w') as fp:
    json.dump(b_data, fp, sort_keys=True, indent=2)

for url in error_urls:
    with open('errors.txt', 'w') as ef:
        ef.write("%s\n" % url)
