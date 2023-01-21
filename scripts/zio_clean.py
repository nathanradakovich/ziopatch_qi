#%%
"""
Goals of workbook:
- summarize patient population
- fix any issues w/improper labels
- summarize how long it takes for patients to get notified
- figure out if any particular subsets of patients fall 
through the cracks (do more specialist-ordered ziopatches
get lost to follow up or do more PCP-ordered?)
- does notification take longer if PCP or specialist orders?
- How often do specialists notify PCPs
"""

#%%
import pandas as pd
import scipy.stats as stats
import numpy as np
from matplotlib import pyplot as plt
import tableone
from zio_config import (cols_i_want,
        col_replace_dic,prov_dic,y_n_cols,
        y_n_dic,
        notification_dic,notifier_dic,reason_dic)
from utils import trimandlower
import seaborn as sns
import tableone 

PATH = "../"
DATA = "data/"

review_df = pd.read_csv(PATH+\
        DATA+'zio_20230116_trimmed.csv',
        encoding="ISO-8859-1")

review_df = trimandlower(review_df)
#%%

review_df = review_df[cols_i_want]
review_df.columns = [col_replace_dic[item] for item in cols_i_want]

#%%
# get time to notification
review_df['time_to_notification'] = pd.to_datetime(review_df['notification_date'],errors='coerce') - \
        pd.to_datetime(review_df['results_date'],errors='coerce') 
review_df['time_to_notification'] = review_df['time_to_notification'].dt.days

# fix all y/n cols:
for col in y_n_cols:
        review_df[col] = review_df[col].map(y_n_dic)
review_df['study_reason'] = review_df['study_reason'].map(reason_dic)
review_df['notification_means'] = review_df['notification_means'].map(notification_dic)
review_df['who_notified'] = review_df['who_notified'].map(notifier_dic)
review_df['ord_prov'] = review_df['ord_prov'].map(prov_dic)

# %%
review_df.to_csv(PATH+DATA+'zio_cleaned.csv')
#%%
# Table one:
t1cols = ['age', 
        # 'study_reason', 
        'ord_prov', 'ord_notified',
       'who_notified',# 'results_date', 'notification_date',
       'notification_means', 'new_af', 
#        'other_findings',
       'change_rec', 'cards_contacted',
       'time_to_notification',
       ]
t1cat = [
        # 'study_reason', 
        'ord_prov', 'ord_notified',
       'who_notified','notification_means', 'new_af', 
       'change_rec', 'cards_contacted'
       ]

mytable = tableone.TableOne(review_df, columns=t1cols, categorical=t1cat, 
        # groupby=groupby, nonnormal=nonnormal, rename=labels, pval=False
        )
print(mytable.tabulate(
        # tablefmt = "fancy_grid"
        ))

#%%
# strip plot
# plt_dic = {'kind':'bar','hue':'ord_prov'}

#%%
def catplt(my_df, x_val,y_val,**kwargs):
        myplt = sns.catplot(data=my_df, x=x_val, y=y_val,
                # **kwargs
                )
        return myplt

catplt(review_df,x_val="time_to_notification",
        y_val="any_af",**plt_dic
        )
#%%


cat_plot = sns.catplot(data=review_df, 
        # kind="bar",
        # title='Time to notification by \nresult and ordering provider', 
        kind="swarm",
        x="time_to_notification", 
        y="new_af", 
        hue="ord_prov"
        )

# plt.legend(loc='upper left')
cat_plot.set_ylabels("Any AF")
cat_plot.set_xlabels("Time to Notification")
plt.title('Time to Notification By Provider')
# plt.savefig(PATH+'time_to_notification.png')
#%%
cat_plot = sns.catplot(data=review_df, 
        kind='swarm',
        x="90dcan", y="new_af",
        hue="ord_prov" 
        # hue="sex"
        )

# plt.legend(loc='upper left')
cat_plot.set_ylabels("New AF?")
cat_plot.set_xlabels("CAN Score")
plt.title('CAN Score')
# plt.savefig(PATH+'CAN_by_new_AF')
# %%
