import bibtexparser as parser
import plotly.graph_objs as go
import seaborn as sns
import pandas as pd
import re
import json
import itertools
import csv


def print_inclusion_exclusion(filepath_included, filepath_interesting, filepath_excluded, filepath_params, name, caption, previous_steps=[], later_steps=[]):

    entries = []
    with open(filepath_params) as paramfile:
        params = json.load(paramfile)

    for filepath in [filepath_included, filepath_excluded, filepath_interesting]:
        with open(filepath) as bibtex_file:
            bib_database = parser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)
            entries.extend(bib_database.entries)

    def get_exluded_entries(entries, criteria):
        print(criteria)
        return sum(any(crit in entry['comments'] for crit in criteria ) for entry  in entries)

    last_included, last_excluded = previous_steps[-1][1]
    

    steps = list(itertools.chain(previous_steps, [(params['exclusion_criteria'][x], (last_included-get_exluded_entries(entries, params['exclusion_criteria'][:x+1]), last_excluded + get_exluded_entries(entries, params['exclusion_criteria'][:x+1]))) for x in range(len(params['exclusion_criteria']))], later_steps))
    steps.append(('Resulting corpus', (steps[-1][1][0], 0)))

    with open('../data/inclusion_exclusion_data.csv', 'w', newline='') as csvfile:
        datawriter = csv.writer(csvfile)
        datawriter.writerow(['Step', 'Total included publications', 'Total exluded publications'])
        [datawriter.writerow([name, inc, exc]) for name, (inc, exc) in steps]
            

    fig = go.Figure()
    fig.add_trace(go.Bar(x=[name for name, (inc, exc) in steps], y=[inc for name, (inc, exc) in steps],
                    base=0,
                    text=[inc for name, (inc, exc) in steps],
                    textposition='auto',
                    marker_color='green',
                    name='Total included publications'))
    fig.add_trace(go.Bar(x=[name for name, (inc, exc) in steps], y=[exc for name, (inc, exc) in steps],
                    base=[-exc for name, (inc, exc) in steps],
                    text=[exc for name, (inc, exc) in steps],
                    textposition='auto',
                    marker_color='crimson',
                    name='Total excluded publications'
                    ))

    fig.write_image('./' + name + '.pdf')

    print(r"\begin{figure}[htbp!]")
    print(r"\centering")
    print(r"\includegraphics[width=1.0\textwidth]{" + name + ".pdf}")
    print(r"""\caption{\label{fig:""" + name + """}%
        """ + caption + """}""")
    print(r"\end{figure}")

print_inclusion_exclusion('../data/stage1_rejected.bib', '../data/stage1_interesting.bib', '../data/stage2.bib', 'inclusion_exclusion.json', 'test', '', previous_steps=[('Sourcing', (400, 0)), ('1. Deduplication', (361, 39))], later_steps=[('2. Deduplication', (83, 417))])