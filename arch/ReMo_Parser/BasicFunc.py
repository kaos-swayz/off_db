#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re

def fetch_html(src_url):
    #function takes url and returns pure html
    sw = " === "
    print(sw + "fetching html from " + src_url + sw)
    r = urllib2.urlopen(src_url)
    html = r.read()
    return html

def r_rest(html,extr):
    #find the extraction spot and return rest of string
    stop_no = html.find(extr) + 1
    rest_html = html[stop_no:]
    return rest_html

def phrase_count(html, x):
    n = 0
    r = 1
    while r > 0:
        r = html.find(x)
        r += 1
        html = html[r:]
        if r <= 0:
            break
        n += 1
    return n

def extract_value(html, extr):
    beg = html.find(">", html.find(extr))
    beg = beg + 1
    value = html[beg:html.find("<", beg)]
    return value

def leave_digits(text):
    if "m2" in text:
        text = text.replace("m2", "")
        results =  re.sub("[^0-9]", "", text)
    else:
        results = re.sub("[^0-9]", "", text)
    if re.search("[0-9]", results):
        return int(results)

def get_float(text):
    results = []
    if re.search(r"[0-9]", text):
        if re.search("\.", text):
            temp = re.findall("\d+\.\d+", text)
        else:
            temp = re.findall("^\d+", text)
        for e in temp:
            if re.search("[0-9]", e):
                results.append(float(e))
    return results

def get_currency(text):
    check = True
    if text[-1] == "2":
        check = False
    if "&#8364;" in text:
        text = text.replace("&#8364;", "euro")
    text = re.sub("[0-9]", "", text)
    text = re.sub("\.", "", text)
    text = re.sub("^ ", "", text)
    if check == False:
        text = text + "2"
    if "euro" in text:
        text = text.replace("euro", "&#8364;")
    if re.search(r"^-", text):
        text = text[3:]
    return text
