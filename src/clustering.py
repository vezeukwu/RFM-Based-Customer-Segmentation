import pandas as pd
from sklearn.cluster import KMeans 
from sklearn.preprocessing import StandardScaler

from src.rfm_analysis import RFM_table

scaler = StandardScaler()
scaled_df = scaler.fit_transform(RFM_table[['recency',	'frequency',	'monetary',	'R_score',	'M_score',	'F_score',	'Total_RFM_score']])


final_model = KMeans(random_state = 1, n_clusters = 4)
final_model.fit(scaled_df)
cluster_assignment = final_model.labels_
RFM_table['Cluster'] = cluster_assignment # type: ignore
RFM_table
