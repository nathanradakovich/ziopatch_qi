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
        col_replace_dic)
import seaborn as sns
import tableone 
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


#%%
# Table one:
t1cols = ['90dcan', 'age','new_af','cont_af','time_to_notification',
        'ord_prov','cards_prov_contact','any_af',]
t1cat = ['new_af','cont_af','ord_prov','cards_prov_contact','any_af']

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
        y="any_af", 
        hue="ord_prov"
        )

plt.legend(loc='upper left')
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
