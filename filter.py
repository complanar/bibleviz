#!/usr/bin/env python3

import helpers

limit = 10 ** 6
referenceLimit = 10 ** 6
minVotes = 6

referenceList = []

r = open("cross_references.txt", "r")

count = 0
referenceCount = 0
r.readline()
for l in r.readlines():
    spl = l.strip().split("\t")
    fromPassage, toPassage, votes = spl[0], spl[1], int(spl[2])

    # filter out whole passages from cross references, only use first verse of reference destination
    to = helpers.parseOsisPassage(toPassage)

    # add reference
    if votes >= minVotes:
        referenceList.append(f"{fromPassage}\t{to['book']}.{to['chapter']}.{to['verse']}\t{votes}\n")
        referenceCount += 1
    
    count += 1
    if count >= limit or referenceCount >= referenceLimit:
        break

r.close()

# write csv
c = open("build/cross_references_filtered.csv","w")
for r in referenceList:
    c.write(r)
c.close()

print(f"Wrote {referenceCount} references.")