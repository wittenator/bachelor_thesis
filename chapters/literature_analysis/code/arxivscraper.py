import arxiv
import json
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

with open('./params.json') as json_file:
	params = json.load(json_file)
	search_string = ' AND '.join( '( ' + ' OR '.join([ f'"{item}"' for item in ors]) + ' )' for ors in params["stage1"])
print(search_string)
# Multi-field queries
result = arxiv.query(search_query=search_string, max_results=100)
print(result[0])

biblist = []
for item in result:
	bibitem = {}
	bibitem['ENTRYTYPE'] = 'article'
	bibitem['ID'] = item['id']
	bibitem['abstract'] = item['summary']
	bibitem['title'] = item['title']
	bibitem['journal'] = 'arxiv'
	bibitem['author'] = ' and '.join([', '.join(author.rsplit(' ', 1)[::-1]) for author in item['authors']])
	bibitem['year'] = str(item['published_parsed'].tm_year)
	bibitem['month'] = str(item['published_parsed'].tm_mon)
	bibitem['url'] = item['pdf_url']
	biblist.append(bibitem)

db = BibDatabase()
db.entries = biblist

writer = BibTexWriter()
with open('../data/arxiv_fulltextsearch.bib', 'w') as bibfile:
    bibfile.write(writer.write(db))


