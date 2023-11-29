#!/usr/bin/env python3

def parseOsisPassage(osisPassage):
    b, c, v = osisPassage.split(".", 2)
    v = v.split("-", 1)[0]
    return {"book": b, "chapter": int(c), "verse": int(v), "bookChapter": f"{b}.{c}"}

def parseReference(ref):
    fromPassage, toPassage, votes = ref
    fromPassage, toPassage = parseOsisPassage(fromPassage), parseOsisPassage(toPassage)
    return {"from": fromPassage, "to": toPassage}