# -*- coding: utf-8 -*-
import re
import sys
from bs4 import BeautifulSoup
import requests
import pprint
from tqdm import tqdm
import json
import string

def find_area(text):
    area_regex_acre = """\d+[.|,]*\d*\s*acre\w*"""
    area_regex_hectare = """\d+[.|,]*\d*\s*hectare"""
    area_regex_ha = """\d+[.|,]*\d*\s*ha"""
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
        print name
        print re.findall(regex, text)
        acres = [conversion(size) for size in re.findall(regex, text)]
        print acres, "\n"
        [all_acres.append(conversion(size)) for size in re.findall(regex, text)]
    # print all_acres
    return max(all_acres)

def find_price(text):
    price_regex = """Price: (.*)? euros"""
    prices = re.findall(price_regex, text)
    price = max([int(p.replace(',','')) for p in prices])
    return price

def get_stats(url):
    text = get_text_from_link(url)
    price = find_price(text)
    area = find_area(text)
    value = price / area
    return {"url": url, "price": price, "area": area, "value": value}

def get_text_from_link(url):
    return requests.get(url).text

print get_stats(sys.argv[1])
