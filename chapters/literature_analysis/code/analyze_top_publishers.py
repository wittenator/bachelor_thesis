import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="ticks", color_codes=True)


def show_top_publishers(filepath, name):
	df = pd.read_csv(filepath)
	df = df.groupby(['Publisher']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
	N = 4
	topn = df.iloc[:N]
	topn.loc['Other'] = [f'{len(df.iloc[N:])} other publishers', df['counts'].iloc[N:].sum()]
	g = sns.catplot(x="Publisher", y='counts', kind="bar", data=topn)
	g.set_xticklabels(rotation=90)
	plt.tight_layout();
	plt.savefig("./" + name + ".pdf", bbox_inches="tight");

	print(r"\begin{figure}[htbp!]")
	print(r"\centering")
	print(r"\includegraphics[width=0.65\textwidth]{" + name +".pdf}")
	print(r"""\caption{\label{fig:""" + name + """}%
		Barplot displaying the distribution of publishers occurring in the meta search results}""")
	print(r"\end{figure}")
	plt.clf()


