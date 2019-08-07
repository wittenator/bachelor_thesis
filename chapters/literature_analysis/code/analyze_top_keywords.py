import bibtexparser as parser
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
sns.set(color_codes=True)
matplotlib.use('TkAgg')

def print_top_keywords(filepath, name):
    with open(filepath) as bibtex_file:
        bib_database = parser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)

    pubdata = pd.DataFrame.from_records(bib_database.entries)
    pubdata["keywords"] = pubdata["keywords"].str.lower()
    pubdata["keywords"] = pubdata["keywords"].str.split(pat =";|,")

    keywords = [item.strip() for sublist in pubdata["keywords"][pubdata['keywords'].notnull()] for item in sublist]
    keywords = pd.DataFrame(data=keywords, columns=["count"])
    keywords = keywords["count"].value_counts()[:20]

    plt.subplots(figsize=(5,4))
    sns.barplot(y=keywords.index, x=keywords, orient='h')

    plt.tight_layout()
    plt.savefig("./" + name + ".pdf", bbox_inches="tight")

    print(r"\begin{figure}[tbp]")
    print(r"\centering")
    print(r"\includegraphics[width=1.0\textwidth]{" + name + ".pdf}")
    print(r"""\caption{\label{fig:""" + name + """}%
        List of the 20 most used tags and their absolute frequency}""")
    print(r"\end{figure}")
    plt.clf()
