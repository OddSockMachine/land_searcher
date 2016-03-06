#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import pprint
from tqdm import tqdm
import json
import string
import requache
import requests

def find_area(text):
    area_regex_acre = """\d+[.|,]*\d*\s*acre\w*"""
    area_regex_hectare = """\d+[.|,]*\d*\s*hectare"""
    area_regex_ha = """\d+[.|,]*\d*\s*ha[^\w]"""
    area_regex_msq = """\d+[.|,]*\d*\s*m2"""
    area_finders = [
        ("acre", area_regex_acre,
        lambda x: float( str(x.split(' ')[0]).replace(',','.').translate(None, string.letters) ) / 1        ),
        ("ha", area_regex_ha,
        lambda x: float( str(x.split(' ')[0]).replace(',','.').translate(None, string.letters) ) / 0.404686 ),
        ("hectare", area_regex_hectare,
        lambda x: float( str(x.split(' ')[0]).replace(',','.').translate(None, string.letters) ) / 0.404686 ),
        ("msq", area_regex_msq,
        lambda x: float( str(x.split(' ')[0]).replace(',','' ).replace("m2", "") ) / 4046.86  ),
        ]
    all_acres = []
    for area in area_finders:
        name, regex, conversion = area
        [all_acres.append(conversion(size)) for size in re.findall(regex, text)]
    return max(all_acres)

def find_price(text):
    price_regex = """Price: (.*)? euros"""
    prices = re.findall(price_regex, text)
    price = max([int(p.replace(',','')) for p in prices])
    price = price * 0.77483
    return price

def get_stats(url):
    try:
        text = get_text_from_link(url)
        price = find_price(text)
        area = find_area(text)
        value = price / area
        return {"url": url, "price": price, "area": area, "value": value}
    except:
        # print "Error with", url
        return

def get_text_from_link(url):
    return requache.get(url)

currency_api_url = "http://api.fixer.io/latest?symbols=USD,GBP"
base_url = "http://pureportugal.co.uk/"
list_url = "http://www.pureportugal.co.uk/listman/exec/search.cgi?search=1&perpage=1000&marknew=7&euro_numbers=0&sort_order=5%2C123%2Cforward&check_created=1&lfield5_min=&lfield5_max=200%2C000&lfield8_keyword=&lfield9_min=&lfield9_max=&lfield2_keyword=&lfield4_keyword=&lfield13_min=&lfield13_max=&lfield30_keyword=&shownew=&search=++Search+Listings++&search=1&marknew=1&euro_numbers=0&lfield1_keyword="
link_css_path = "html body div#content div.row span.image a[href]"

r  = requests.get(list_url )
data = r.text
soup = BeautifulSoup(data, "lxml")
links = [base_url+link.get('href') for link in soup.select(link_css_path)]

data = []
for link in tqdm(links):
    # print link
    info = get_stats(link)
    if info:
        data.append(info)

with open("data.json", "w") as datafile:
    json.dump(data, datafile)
