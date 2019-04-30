import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="ticks", color_codes=True)


def show_top_publishers(filepath):
	df = pd.read_csv(filepath)
	df = df.groupby(['Publisher']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
	print(df)
	N = 4
	topn = df.iloc[:N]
	topn.loc['Other'] = [f'{len(df.iloc[N:])} other publishers', df['counts'].iloc[N:].sum()]
	print(topn)
	g = sns.catplot(x="Publisher", y='counts', kind="bar", palette="ch:.25", data=topn);
	g.set_xticklabels(rotation=90)
	plt.tight_layout();
	plt.show();


