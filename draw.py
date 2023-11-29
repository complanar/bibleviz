#!/usr/bin/env python3

import csv
import json
import easygraphics as eg

import helpers

chaptersFile = "chapter_verses.csv"
referencesFile = "build/cross_references_filtered.csv"
sortedReferencesFile = "build/cross_references_sorted.json"
outputImageFile = "references.png"

#screen_width, screen_height = 2560, 1536
screen_width, screen_height = 12000, 7200
margin = 55
headless = True

readLimit = 10 ** 5
drawLimit = 10 ** 5
hueShift = 190
saturation = 160
value = 230
alpha = 100
lineWidth = 0.25

chapterIndexCache = {}

def getChapterIndex(chapters, osisID):
    global chapterIndexCache
    # add to cache if not already in
    if osisID not in chapterIndexCache:
        for i in range(len(chapters)):
            if chapters[i][0] == osisID:
                chapterIndexCache[osisID] = i
                return i
        return -1
    return chapterIndexCache[osisID]

def getInsertIndex(arcs, offset, distance):
    count = len(arcs)
    if count > 1:
        middle = count // 2
        refDistance = arcs[middle]['refDistance']
        if abs(distance) <= abs(refDistance): # left half
            half = arcs[:middle]
        else: # right half
            half = arcs[middle:]
            offset = offset + middle
        index = getInsertIndex(half, offset, distance)
    else:
        if len(arcs) == 0 or abs(distance) <= abs(arcs[0]['refDistance']):
            return offset
        else:
            return offset + 1
    
    return index

def buildArcData(sortedReferencesFile, chapters):
    print("Calculating arc data ...")
    # try to load sorted references from file
    try: 
        print("Read arc data from json file ...")
        jFile = open(sortedReferencesFile)
        arcs = json.load(jFile)
        jFile.close()
    # Read references from unsorted csv file
    except:
        print("An error occurred while reading arc data. Recalculating ...")
        referencesFileHandle = open(referencesFile)
        referencesCsv = csv.reader(referencesFileHandle, delimiter="\t")
        references = [ row for row in referencesCsv ]
        referencesFileHandle.close()

        arcs = []

        readCount = 0
        for i in range(len(references)):
            r = references[i]
            ref = helpers.parseReference(r)
            fromPos = getChapterIndex(chapters, ref['from']['bookChapter'])
            toPos = getChapterIndex(chapters, ref['to']['bookChapter'])
            
            # filter cross references to non-existent chapters (e.g. Mal.4)
            if fromPos == -1 or toPos == -1:
                print(f"Warning: Chapter does not exist in reference {ref['from']['bookChapter']} → {ref['to']['bookChapter']}")
                continue
            refDistance = toPos - fromPos

            arcData = { 'from': ref['from'], 'to': ref['to'], 'fromPos': fromPos, 'toPos': toPos, 'refDistance': refDistance }

            # insert sorted, ascending by refDistance
            pos = getInsertIndex(arcs, 0, refDistance)
            arcs.insert(pos, arcData)

            readCount += 1
            if readCount >= readLimit:
                break
        
        print(f"Found {readCount} cross references.")
    
        # write sorted references to json
        print("Write data to json file …")
        jFileHandle = open(sortedReferencesFile, "w")
        jRef = json.dumps(arcs)
        jFileHandle.write(jRef)
        jFileHandle.close()


def drawArcs(chapters):
    chapterCount = len(chapters)
    chapterWidth = (screen_width - 2 * margin) / chapterCount
    centerY = int(screen_width / 2 + 0.75 * margin)


    ### calculate reference arc data ###
    arcs = buildArcData(sortedReferencesFile, chapters)

    ### draw arcs ###
    print("Draw arcs ...")
    #arcs.reverse() # remove comment to draw widest arcs first instead of narrowest arcs
    drawCount = 0
    duplicateCount = 0
    eg.set_line_width(lineWidth)
    
    prevArc = None
    for i in range(len(arcs)):
        arc = arcs[i]

        # ignore chapter wise duplicates?
        if prevArc != None and prevArc['from']['bookChapter'] == arc['from']['bookChapter'] and prevArc['to']['bookChapter'] == arc['to']['bookChapter']:
            duplicateCount += 1
            #print("Ignore duplicate")
            #continue

        if abs(arc['refDistance']) > 0:
            # color
            color = eg.color_hsv((int(abs(arc['refDistance']) / chapterCount * 720) + hueShift) % 360, saturation, value, alpha)
            eg.set_color(color)

            # position and size
            fromX = arc['fromPos'] * chapterWidth + margin + 0.5 * chapterWidth
            toX = arc['toPos'] * chapterWidth + margin + 0.5 * chapterWidth
            radians = int(abs(fromX - toX) / 2)
            centerX = int((fromX + toX) / 2)

            # draw arc
            eg.arc(centerX, centerY, 0, 180, radians, radians)

            drawCount += 1
        
        prevArc = arc
        if drawCount >= drawLimit:
            break
    print(f"Drew {drawCount} arcs, found {duplicateCount} duplicates.")

def drawChapters(chapters):
    print("Draw chapters ...")
    chapterCount = len(chapters)
    chapterWidth = (screen_width - 2 * margin) / chapterCount
    chapterMaxHeight = screen_height - screen_width / 2 - 2 * margin
    y = int((screen_width / 2) + margin)

    bookCount = 0
    lastBook = ''
    for chapter in chapters:
        book, ch = chapter[0].split(".")
        if lastBook != book:
            lastBook = book
            bookCount += 1

        if bookCount % 2 == 1:
            color = eg.color_gray(255)
        else:
            color = eg.color_gray(255, 180)

        eg.set_fill_color(color)
        x = getChapterIndex(chapters, chapter[0]) * chapterWidth + margin
        chapterHeight = int(chapter[1] / 176 * chapterMaxHeight) # 176 verses → Psalm 119
        eg.fill_rect(x + 1, y, x + chapterWidth - 1, y + chapterHeight)

def main():
    # read chapter info
    chaptersFileHandle = open(chaptersFile)
    chaptersCsv = csv.reader(chaptersFileHandle, delimiter="\t")
    chapters = []
    for row in chaptersCsv:
        if row[0] != "chapter":
            chapters.append((row[0], int(row[1])))
    chaptersFileHandle.close()

    eg.init_graph(screen_width, screen_height, headless = headless)
    # fill background
    eg.set_fill_color(eg.Color.BLACK)
    eg.fill_rect(0,0,screen_width,screen_height)
    # draw arcs
    drawArcs(chapters)
    # draw chapters
    drawChapters(chapters)
    if not headless:
        eg.pause()
    print("Save image ...")
    eg.save_image(outputImageFile)
    eg.close_graph()

eg.easy_run(main)
