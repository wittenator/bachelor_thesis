import pandas as pd
import numpy as np
import plotly
from math import floor, pow
import plotly.graph_objs as go

def print_type_distribution(excel_name, name, caption):

	df = pd.read_excel(excel_name)

	df = df['Type'].value_counts()
	df.to_csv('../data/type_dist_data.csv')

	fig = go.Figure(data=[go.Pie(labels=df.index, values=df, textinfo='value', textfont_size=20)])

	layout = dict(width = 800, height = 600, autosize= False, margin = go.layout.Margin(
	l = 150,
	r = 50,
	b = 150,
	t = 50,
	pad = 4))

	fig.write_image('./' + name + '.pdf')

	print(r"\begin{figure}[htbp!]")
	print(r"\centering")
	print(r"\includegraphics[width=1.0\textwidth]{" + name + ".pdf}")
	print(r"""\caption{\label{fig:""" + name + """}%
        """ + caption + """}""")
	print(r"\end{figure}")


print_type_distribution('../data/mapping.xlsx', 'test', 'caption')
