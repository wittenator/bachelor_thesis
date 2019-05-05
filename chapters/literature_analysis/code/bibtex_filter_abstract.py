import bibtexparser as parser
import json

with open('../data/stage1.bib') as bibtex_file:
    bib_database = parser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)

with open('./params.json') as json_file:
    params = json.load(json_file);

print(params)
bad_entries = []
filtered_entries = []

for entry in bib_database.entries:
    if not 'abstract' in entry:
        bad_entries.append(entry)
    else:
        text = (entry['abstract'] + " " + entry['title']).lower()
        if all(any(keyword in text for keyword in synonyms) for synonyms in params['ANDOR']) or any(keyword in text for keyword in params['OR']):
            filtered_entries.append(entry)

with open('../data/stage2.bib', 'w') as bibtex_file:
    bib_database.entries = filtered_entries
    parser.dump(bib_database, bibtex_file)

with open('../data/stage-1-rest.bib', 'w') as bibtex_file:
    bib_database.entries = bad_entries
    parser.dump(bib_database, bibtex_file)
