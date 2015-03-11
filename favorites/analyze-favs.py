#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt

percent_dict = {}
df = pd.read_csv('interaction-counts.csv')
nr_comment_count = df['%comment_and_favorite']
for row in nr_comment_count:
    if row not in percent_dict:
        percent_dict[row] = 0
    percent_dict[row] += 1
percent_df = pd.Series(percent_dict, name='percent')
print percent_df
plt.figure()
percent_df.plot(kind='bar')
plt.show()