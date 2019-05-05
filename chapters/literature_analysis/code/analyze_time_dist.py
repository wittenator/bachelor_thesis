import bibtexparser as parser
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import datetime
sns.set(color_codes=True)

def print_time_dist(filepath, name):
    with open(filepath) as bibtex_file:
        bib_database = parser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)

    pubdata = pd.DataFrame.from_records(bib_database.entries)
    #pubdata.year = pd.to_numeric(pubdata.year)
    pubdata['year'] = pd.to_datetime(pubdata['year'])
    time_dist = pubdata.year.value_counts()

    plt.subplots(figsize=(8,4))
    ax = sns.barplot(time_dist.index, time_dist.values)
    fig = ax.get_figure()
    #ax.xaxis_date()
    #set ticks every week
    #ax.xaxis.set_major_locator(mdates.MonthLocator())
    #set major ticks format
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    fig.autofmt_xdate()


    plt.tight_layout()
    plt.savefig(name, bbox_inches="tight")

    print(r"\begin{figure}[tbp]")
    print(r"\centering")
    print(r"\includegraphics[width=1.0\textwidth]{" + name + "}")
    print(r"""\caption{\label{fig:publisher_distribution}%
    	Barplot displaying the distribution of publishers occurring in the meta search results}""")
    print(r"\end{figure}")
    plt.clf()

#print_time_dist('../data/stage1.bib', 'test.pdf')