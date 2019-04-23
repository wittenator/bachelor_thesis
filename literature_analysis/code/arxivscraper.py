import arxiv
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


search_query = [['explainability', 'explainable', 'explanation', 'interpretability', 'interpretable', 'interpretation'], ['machine learning', 'neural network']]
search_string = ' AND '.join( '( ' + ' OR '.join([ f'all:"{item}"' for item in ors]) + ' )' for ors in search_query)
print(search_string)
# Multi-field queries
result = arxiv.query(search_query=search_string)
print(result[0])

biblist = []
for item in result:
	bibitem = {}
	bibitem['ENTRYTYPE'] = 'article'
	bibitem['ID'] = item['id']
	bibitem['abstract'] = item['summary']
	bibitem['title'] = item['title']
	bibitem['journal'] = 'arxiv'
	bibitem['author'] = ', '.join(item['authors'])
	bibitem['year'] = str(item['published_parsed'].tm_year)
	bibitem['month'] = str(item['published_parsed'].tm_mon)
	bibitem['url'] = item['pdf_url']
	biblist.append(bibitem)

db = BibDatabase()
db.entries = biblist

writer = BibTexWriter()
with open('../data/bibtex.bib', 'w') as bibfile:
    bibfile.write(writer.write(db))