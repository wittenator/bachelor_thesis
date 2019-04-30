import bibtexparser as parser
import json

with open('stage3.bib') as bibtex_file:
    bib_database = parser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)

entries = []

for entry in bib_database.entries:
    if 'abstract' in entry:
        entries.append({"title":entry["title"], "abstract":entry["abstract"]})

print(entries)
with open('stage3.json', 'w') as json_file:
    json.dump(entries,json_file)