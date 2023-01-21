#%%
import pandas as pd
import scipy.stats as stats
import numpy as np
from matplotlib import pyplot as plt

PATH = "../"
DATA = "data/"
#%% 
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
       'ord_notified', 
      'who_notified', 
    #   'results_date', 'notification_date',
       'notification_means', 
       'new_af', 
       'other_findings', 
       'question_answered',
       'change_rec', 
       'cards_contacted', 
       'time_to_notification'
        ]


sankey_df = review_df[limited_cols]

#%%
# Define categorical columns



# 



# Functions for stats from columns



# 




# 

#