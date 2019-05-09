import bibtexparser as parser
import json
import sys

merged = []
for file in sys.argv:
    with open(file) as bibtex_file:
        bib_database = parser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)
        merged.extend(bib_database.entries)

with open('../data/stage1.bib', 'w') as bibtex_file:
    bib_database.entries = merged
    parser.dump(bib_database, bibtex_file)
