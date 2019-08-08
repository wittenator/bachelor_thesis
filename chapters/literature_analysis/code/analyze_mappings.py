import pandas as pd
import numpy as np
import plotly
from math import floor, pow
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.io as pio

def print_mapping(excel_name, name, caption, name_x_axis, name_y_axis):

	#define thresholds for renaming category to 'other' in percent
	threshold_x = 5
	threshold_y = 5

	df = pd.read_excel(excel_name)

	totalcount = np.ma.count(df[name_x_axis])
	th_x = floor(totalcount / 100.0 * threshold_x)
	th_y = floor(totalcount / 100.0 * threshold_y)

	x = np.unique(df[name_x_axis].astype(str), return_counts = True)
	for val in np.nonzero(x[1]<th_x):
	    df[name_x_axis] =  df[name_x_axis]
	    
	y = np.unique(df[name_y_axis].astype(str), return_counts = True)
	for val in np.nonzero(y[1]<th_y):
	    df[name_x_axis] =  df[name_x_axis]

	pivot_list = []
	for x_val in x[0]:
	    for hits in np.nonzero(df[name_x_axis] == x_val):
	        for y_val in y[0]:
	            if int(np.ma.count(np.nonzero(df[name_y_axis][hits] == y_val))) > 0:
	                pivot_list.append([int(np.ma.count(np.nonzero(df[name_y_axis][hits] == y_val))), x_val, y_val])
	pivot_list = np.transpose(pivot_list).tolist()  

	data = [
	    {
	        'x': pivot_list[1],
	        'y': pivot_list[2],
	        'mode':'markers+text',
	        'marker': {
	            'size': list(map((lambda x: pow(x,0.6)*20), map(int, pivot_list[0]))),
	        },
	        'text': pivot_list[0],
	        'textposition':'middle center'
	    }
	]

	layout = dict(width = 800, height = 600, autosize= False, margin = go.layout.Margin(
	l = 150,
	r = 50,
	b = 150,
	t = 50,
	pad = 4))

	fig = dict(data = data, layout = layout)

	pio.write_image(fig, './' + name + '.pdf')

	print(r"\begin{figure}[htbp!]")
	print(r"\centering")
	print(r"\includegraphics[width=1.0\textwidth]{" + name + ".pdf}")
	print(r"""\caption{\label{fig:""" + name + """}%
        """ + caption + """}""")
	print(r"\end{figure}")
