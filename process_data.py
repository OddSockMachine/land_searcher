#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
import lifter
import json

with open("data.json", "r") as datafile:
    data = json.load(datafile)

def format_data(data):
    return "{} acres for £{} - {}".format(int(data['area']), int(data['price']), data['url'])

def output_all(properties):
    for p in properties:
        print format_data(p)
    print "\n"


Property = lifter.models.Model('Property')
manager = Property.load(data)

value_order = manager.order_by(Property.value)[:10]
print "Best Value:"
output_all(value_order)

cheapest = manager.order_by(Property.price).filter(Property.area > 1)[:10]
print "Cheapest:"
output_all(cheapest)

largest = manager.order_by(~Property.area)[:15]
print "Largest:"
output_all(largest)
