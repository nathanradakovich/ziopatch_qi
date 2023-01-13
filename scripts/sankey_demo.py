#%%
import plotly.graph_objects as go
import plotly.express as pex
import pandas as pd
import numpy as np

nz_migration = pd.read_csv("../data/migration_nz.csv")

#%%

nz_migration = nz_migration[nz_migration["Measure"]!="Net"] ## Removing Entries related to "Net Total"
nz_migration = nz_migration[~nz_migration["Country"].isin(["Not stated", "All countries"])] ## Removing entries with No Details or all countries

nz_migration_grouped = nz_migration.groupby(by=["Measure","Country"]).sum()[["Value"]]
nz_migration_grouped = nz_migration_grouped.reset_index()

nz_migration_grouped.head(10) ## Displaying first 10 rows

#%%
continents = ["Asia", "Australia","Africa and the Middle East","Europe", "Americas", "Oceania"]

continent_wise_migration = nz_migration_grouped[nz_migration_grouped.Country.isin(continents)]

## All chart nodes
all_nodes = continent_wise_migration.Measure.values.tolist() + continent_wise_migration.Country.values.tolist()

## Indices of sources and destinations
source_indices = [all_nodes.index(measure) for measure in continent_wise_migration.Measure] ## Retrieve source nodes indexes as per all nodes list.
target_indices = [all_nodes.index(country) for country in continent_wise_migration.Country] ## Retrieve destination nodes indexes as per all nodes list.

fig = go.Figure(data=[go.Sankey(
                        # Define nodes
                        node = dict(
                          label =  all_nodes,
                          color =  "red"
                        ),

                        # Add links
                        link = dict(
                          source =  source_indices,
                          target =  target_indices,
                          value =  continent_wise_migration.Value,
                        )
                    )
                ])

fig.update_layout(title_text="Population Migration between New Zealand and Other Continents",
                  font_size=10)
fig.show()

#%%
#Graph of # with new afib who were notified c/w no new AF

label_list = ['source', 'dest','count']

sankey_list = [
    ['PMD','PMD Notified',20],
    ['Specialist','PMD Notified',10],
    ['Specialist','Specialist Notified',10],
    ['PMD Notified','On-time Notification',35],
    ['Specialist Notified','On-time Notification',5],
    ['PMD Notified','Delayed Notification',5],
    ['Specialist Notified','Delayed Notification',5],
]

sankey_df = pd.DataFrame(sankey_list, columns=label_list)

#%%

## All chart nodes
all_nodes = sankey_df.source.values.tolist() +\
     sankey_df.dest.values.tolist()

#%%
## Indices of sources and destinations
source_indices = [all_nodes.index(source) for source in sankey_df.source] ## Retrieve source nodes indexes as per all nodes list.
target_indices = [all_nodes.index(dest) for dest in sankey_df.dest] ## Retrieve destination nodes indexes as per all nodes list.

#%%

fig = go.Figure(data=[go.Sankey(
                        # Define nodes
                        node = dict(
                          label =  all_nodes,
                          
                        ),

                        # Add links
                        link = dict(
                          source =  source_indices,
                          target =  target_indices,
                          value =  sankey_df['count'],
                        )
                    )
                ])

fig.update_layout(title_text="Population Migration between New Zealand and Other Continents",
                  font_size=10)
fig.show()


#%%

import holoviews as hv
hv.extension('bokeh')


hv.Sankey(sankey_df)

