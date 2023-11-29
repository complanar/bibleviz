#!/usr/bin/env python3

import xml.etree.ElementTree as ET

osisFile = "Elberfelder 2003.osis.xml"
ns = '{http://www.bibletechnologies.net/2003/OSIS/namespace}'
chapterVerses = []

tree = ET.parse(osisFile)
root = tree.getroot()

for chapter in root.iter(ns + 'chapter'):
    verses = 0
    for verse in chapter.findall(ns + 'verse'):
        verses += 1
    chapterVerses.append(f"{chapter.attrib['osisID']}\t{verses}")
    print(f"Found {verses} verses in chapter {chapter.attrib['osisID']}")

c = open("chapters.csv", "w")
c.write("chapter\tverses\n")
for chapter in chapterVerses:
    c.write(chapter + "\n")
c.close()
