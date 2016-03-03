# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:19:15 2016

@author: C
"""
import csv

#with open("MIT Tweet Mining.csv", "rb") as f:
#    reader = csv.reader(f, delimiter="\t")
#    for i, line in enumerate(reader):
#        print 'line[{}] = {}'.format(i, line)

IDs = []

with open('MIT Tweet Mining.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        IDs.append(row['Tweet ID'])

import collections
print [item for item, count in collections.Counter(IDs).items() if count > 1]
