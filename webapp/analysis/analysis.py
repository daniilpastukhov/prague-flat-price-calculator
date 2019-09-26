import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

prague_info = pd.read_csv('../data/flats_prague_numeric.csv')
brno_info = pd.read_csv('../data/flats_brno_numeric.csv')

plt.figure(figsize=(16, 6))
g = sns.relplot(x='size', y='price', data=prague_info.sort_values('locality'), hue='locality', palette='muted',
                size='price', sizes=(2, 250), alpha=.5, height=8)
plt.ylabel('Price (per month)')
plt.xlabel('Size')

prague_info.groupby('type').agg()