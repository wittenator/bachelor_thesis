import bibtexparser as parser
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
import seaborn as sns
import pandas as pd
import datetime
import numpy as np
sns.set(color_codes=True)

def print_time_dist(filepath, name):
    with open(filepath) as bibtex_file:
        bib_database = parser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)

    pubdata = pd.DataFrame.from_records(bib_database.entries)
    pubdata['year'] = pd.to_datetime(pubdata['year'])
    time_dist = pubdata.year.value_counts()

    fig, ax = plt.subplots()
    ax.bar(date2num(time_dist.index), time_dist.values, width=365)
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_yscale('log')
    fig.autofmt_xdate()


    plt.tight_layout()
    plt.savefig("./" + name + ".pdf", bbox_inches="tight")

    print(r"\begin{figure}[tbp]")
    print(r"\centering")
    print(r"\includegraphics[width=0.8\textwidth]{" + name + ".pdf}")
    print(r"""\caption{\label{fig:""" + name + """}%
    	Barplot displaying the distribution of publishers occurring in the meta search results}""")
    print(r"\end{figure}")
    plt.clf()
