#%%
"""
Make a sankey diagram that summarizes ziopatch workflow
"""

#%%
import pandas as pd
import scipy.stats as stats
import numpy as np
from matplotlib import pyplot as plt
from zio_config import (cols_i_want,
        col_replace_dic)
import seaborn as sns
import tableone 
import holoviews as hv

import plotly.graph_objects as go
import plotly.express as pex


#%%
PATH = "../"
DATA = "data/"

review_df = pd.read_csv(PATH+\
        DATA+'zio_review_20221215.csv',
        encoding="ISO-8859-1")

review_df = review_df[cols_i_want]
review_df.columns = [col_replace_dic[item] for item in cols_i_want]
#%%
review_df['time_to_notification'] = pd.to_datetime(review_df['date_pt_told'],errors='coerce') - \
        pd.to_datetime(review_df['comp_time'],errors='coerce') 
review_df['time_to_notification'] = review_df['time_to_notification'].dt.days

review_df['any_af'] = ((review_df['new_af'] == 'Y') | 
        (review_df['cont_af'] == 'Y'))
review_df['any_af'] = np.where(review_df['any_af'], 'Y', 'N')
        
# %%
#Graph of # with new afib who were notified c/w no new AF
limited_cols =['ord_prov', 
        # 'ord_notified', 
        'any_af',
        'notifying_party', 
        # 'new_af', 'rec_given',
#        'cards_prov_contact', 'notes', 'reviewer', 'time_to_notification',
       ]

replace_prov = {'Inpatient':'Other', 'CT Surg':"Other"}

replace_not = {'no notifcation':'nobody', 'no one':'nobody',
        'N/a':'nobody',
        'PCP':'primary_care',
       'Seen in-patient':'other', 
       'Discussed at Cardiology visit':'cardiology',
       'Patient called, spoke to Cardiology':'cardiology', 
       'PACT RN':'other',
       'Another member of CT Surg team':'other', 'Cardiology':'cardiology'}

sankey_df = review_df[limited_cols].fillna('unknown')
sankey_df = sankey_df[sankey_df['ord_prov']!='unknown']
sankey_df.ord_prov = sankey_df.ord_prov.replace(replace_prov)
sankey_df.notifying_party = sankey_df.notifying_party.replace(replace_not)

#%%
group_list = []
group_cols = ['src','trgt','cnt']
for i in range(len(limited_cols)-1):
        col_a = limited_cols[i]
        col_b = limited_cols[i+1]
        temp_list = sankey_df.groupby([col_a,col_b]).size().reset_index().values.tolist()
        group_list = group_list + temp_list

group_df = pd.DataFrame(group_list,columns=group_cols)
group_df
#%%

# df_grouped = sankey_df.groupby(limited_cols).size().reset_index()
# df_grouped.columns = limited_cols+["count"]

#%%

import holoviews as hv
hv.extension('bokeh')

hv.Sankey(group_df)


#%%


#%%
# label_list = ['source', 'dest','count']

# sankey_list = [
#     ['PMD','PMD Notified',20],
#     ['Specialist','PMD Notified',10],
#     ['Specialist','Specialist Notified',10],
#     ['PMD Notified','On-time Notification',35],
#     ['Specialist Notified','On-time Notification',5],
#     ['PMD Notified','Delayed Notification',5],
#     ['Specialist Notified','Delayed Notification',5],
# ]
# sankey_df = pd.DataFrame(sankey_list, columns=label_list)



fig = go.Figure(data=[
                    go.Sankey(
                        node = dict(
                                pad = 20,
                                thickness = 20,
                                line = dict(color = "black", width = 1.0),
                                # label =  all_nodes,
                                # color =  node_colors,
                               ),
                        link = dict(
                               source =  list(sankey_df['source']),
                               target =  list(sankey_df['dest']),
                               value =  list(sankey_df['count']),,
                            #    color = edge_colors
                               )
                         )
                    ])

fig.update_layout(title_text="User Journey on Website",
                  height=600,
                  font=dict(size = 10, color = 'white'),
                  plot_bgcolor='black', paper_bgcolor='black')

fig.show()

