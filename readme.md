# Visualization of biblical cross references

Chris Harrison’s influencial vizualization of biblical cross references (https://www.chrisharrison.net/index.php/Visualizations/BibleViz) inspired me to create a remake of the image using [another database of cross references](https://www.openbible.info/labs/cross-references/). This is to be considered more a kind of practise than a substitute or even an enhancement. 

The code may be in poor quality! This is currently in proof-of-concept-state.

## Original

![https://chrisharrison.net/projects/bibleviz/BibleVizArc7WiderOTNTsmall.png](https://chrisharrison.net/projects/bibleviz/BibleVizArc7WiderOTNTsmall.png)

## Remake

![references-1200x720.jpg](references-1200x720.jpg)



## Dependencies
The following Python modules are used and therefore must be available at the build system:
- xml, csv, json (standard python modules, shipped with almost every Python distribution)
- easygraphics (available via `pip`) 

## File structure and python scripts

- `cross_references.txt`: Contains 344.799 cross references in some kind of tab separated csv table with the following fields: `From Verse`, `To Verse`, `Votes`, uses OSIS naming convention.
- `cross_references.csv`: Contains a list of 68.162 cross references with the highest rating. Was generated out of `cross_references.txt` with `filter.py`. Please have a look at `filter.py`, modify it to your needs to create a different filtered list.
- `chapter-verses.csv`: Contains a list of all chapters of the bible with the corresponding number of the contained verses, also uses OSIS naming convention. It was generated out of an Elberfelder 2003 XML module I can not share here due to copyright restrictions.
- `filter.py`: Short script to filter all cross references. Does not contain any fancy filtering algorithms, just compares all Please modify to your needs to filter the list differently.
- `helpers.py`: Helper functions used in `filter.py` and `draw.py`.
- `draw.py`: Heart of this repository. Draws arcs and saves image. 
