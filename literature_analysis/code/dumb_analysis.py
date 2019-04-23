import bibtexparser as parser
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly import tools

sns.set(color_codes=True)
matplotlib.use('TkAgg')

with open('stage3_proto.bib') as bibtex_file:
    bib_database = parser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)

pubdata = pd.DataFrame.from_records(bib_database.entries)
pubdata["keywords"] = pubdata["keywords"].str.lower()
pubdata["keywords"] = pubdata["keywords"].str.split(",")
print(pubdata.keys())
pubdata["date"] = pubdata["date"].str.slice(0,4)

fig, axs = plt.subplots(ncols=3)
sns.countplot(x="date", data=pubdata, ax=axs[0])
publication = []
for item in pubdata.iterrows():
    if(item[1]['ENTRYTYPE'] == 'article'):
        publication.append(item[1]['journaltitle'])
    elif(item[1]['ENTRYTYPE'] == 'inproceedings'):
        publication.append(item[1]['publisher'] if item[1]['publisher'] else None)
    elif(item[1]['ENTRYTYPE'] == 'techreport'):
        publication.append(item[1]["institution"])
    else:
        print('WARNING: Unknown Publication Type')
        publication.append('null')

publication = list(map(lambda x: "Unknown" if not isinstance(x, str) else x ,publication))

keywords = [item.strip() for sublist in pubdata["keywords"][pubdata['keywords'].notnull()] for item in sublist]
keywords = pd.DataFrame(data=keywords, columns=["key"])
keywords = keywords["key"].value_counts()[:20]

publication = pd.DataFrame(data = publication, columns=["publication"])
publication = publication["publication"].value_counts()
print(publication)
publication = publication.to_dict()

publication_others_collapsed = dict(Others = 0)

for item in publication:
    if(publication[item] < 2):
        publication_others_collapsed["Others"] += 1
    else:
        publication_others_collapsed[item] = publication[item]

publication = pd.Series(publication_others_collapsed)

print(publication)
print(keywords)
print(pubdata['date'].value_counts())

# sns.barplot(x=keywords.index, y=keywords, ax=axs[1])
# sns.barplot(x=publication.index, y = publication, ax=axs[2])

# for ax in fig.axes:
#     matplotlib.pyplot.sca(ax)
#     plt.xticks(rotation=90)

# plt.show()

year_data = go.Bar(
    x=pubdata['date'].value_counts().index,
    y=pubdata['date'].value_counts(),
    text=pubdata['date'].value_counts(),
    textposition = 'auto',
    textfont=dict(
        color='#ffffff',
        size=18
    )
)

publication_data = go.Bar(
    x=publication.index,
    y=publication,
    text=publication,
    textposition = 'auto',
    textfont=dict(
        color='#ffffff',
        size=18
    )
)

keywords_data = go.Bar(
    x=keywords.index,
    y=keywords,
    text=keywords,
    textposition = 'auto',
    textfont=dict(
        color='#ffffff',
        size=10
    )
)

figure = tools.make_subplots(rows=1, cols=3, subplot_titles=('Publication Year','Keywords', 'Publications'))

figure.append_trace(year_data, 1, 1)
figure.append_trace(keywords_data,1, 2)
figure.append_trace(publication_data, 1, 3)
figure['layout'].update(
    height=1000, 
    width=1800, 
    showlegend=False,
    margin=go.Margin(
        l=150,
        r=150,
        b=200,
        t=100,
        pad=4
    )
)

py.offline.plot(figure, auto_open=True)