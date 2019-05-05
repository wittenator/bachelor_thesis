import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="ticks", color_codes=True)


def show_top_publishers(filepath):
	df = pd.read_csv(filepath)
	df = df.groupby(['Publisher']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
	N = 4
	topn = df.iloc[:N]
	topn.loc['Other'] = [f'{len(df.iloc[N:])} other publishers', df['counts'].iloc[N:].sum()]
	g = sns.catplot(x="Publisher", y='counts', kind="bar", data=topn)
	plt.xticks(rotation=90)
	plt.tight_layout();
	plt.savefig("./myplot.pdf", bbox_inches="tight");

	print(r"\begin{figure}[tbp]")
	print(r"\centering")
	print(r"\includegraphics[width=0.65\textwidth]{myplot.pdf}")
	print(r"""\caption{\label{fig:publisher_distribution}%
		Barplot displaying the distribution of publishers occurring in the meta search results}""")
	print(r"\end{figure}")
	plt.clf()


