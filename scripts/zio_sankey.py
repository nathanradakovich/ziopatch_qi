#%%
import pandas as pd
import scipy.stats as stats
import numpy as np
from matplotlib import pyplot as plt
import tableone

import seaborn as sns
import tableone 

PATH = "../"
DATA = "data/"

review_df = pd.read_csv(PATH+\
        DATA+'zio_cleaned.csv',
        # encoding="ISO-8859-1"
        )

# %%
#Graph of # with new afib who were notified c/w no new AF
limited_cols =[
        # 'city', 'state', 'age', 
        'study_reason', 
        'ord_prov',
#        'ord_notified', 
      'who_notified', 
#       'results_date', 'notification_date',
       'notification_means', 
       'new_af', 
#        'other_findings', 
#        'question_answered',
#        'change_rec', 
#        'cards_contacted', 
#        'time_to_notification'
        ]
need_entries = [
        'ord_prov',
        # 'new_af'
]
# trim our data frame to remove rows with missing data
# in selected columns:
sankey_df = review_df[limited_cols].fillna('unknown')

for col in need_entries:
        sankey_df = sankey_df[sankey_df[col]!='unknown']

# addend unique names per column in sankey_df to fix
# cyclic reference issues:
# df['col'] = 'str' + df['col'].astype(str)
cnt = 0
for col in sankey_df.columns:
        sankey_df[col] = sankey_df[col] + f'{cnt}'
        cnt = cnt + 1
#%%
# group by colmns, then put together a list with every
# combination between adjacent columns:
group_list = []
group_cols = [f'node{i}' for i in range(len(limited_cols))]
node_cols = ['src','dst','ct']
for i in range(len(limited_cols)-1):
        col_a = limited_cols[i]
        col_b = limited_cols[i+1]
        temp_list = sankey_df.groupby([col_a,col_b]).size().reset_index().values.tolist()
        group_list = group_list + temp_list

group_df = pd.DataFrame(group_list,columns=node_cols)
group_df

#%%
import holoviews as hv
hv.extension('bokeh')
hv.Sankey(group_df)