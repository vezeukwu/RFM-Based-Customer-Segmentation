import pandas as pd

df = pd.read_csv('Output/Cleaned_df.csv')  # adjust path as needed

# Convert TransactionDate to datetime
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])

# Get latest transaction date
day = df['TransactionDate'].max()

day = df['TransactionDate'].max()
days = df['TransactionDate'].min()
recency = df.groupby(['CustomerID']).agg({'TransactionDate': lambda x: ((day - x.max()).days) +1})
frequency = df.drop_duplicates(subset = 'TransactionID').groupby(['CustomerID'])[['TransactionID']].count()
monetary = df.groupby('CustomerID')[['TransactionAmount (INR)']].sum()

RFM_table = pd.concat([recency, frequency, monetary], axis = 1)
RFM_table = RFM_table.rename(columns = {'TransactionDate': 'recency', 'TransactionID': 'frequency', 'TransactionAmount (INR)': 'monetary'})

quantile = RFM_table[['recency', 'frequency', 'monetary']].quantile(q = [0.25, 0.5, 0.75]).to_dict()

def assign_R_score(x, feature):
    if x <= quantile[feature][0.25]:
        return 4
    elif x <= quantile[feature][0.5]:
        return 3
    elif x <= quantile[feature][0.75]:
        return 2
    else:
        return 1

def assign_M_score(x, feature):
    if x <= quantile[feature][0.25]:
        return 1
    elif x <= quantile[feature][0.5]:
        return 2
    elif x <= quantile[feature][0.75]:
        return 3
    else:
        return 4
   
def cust_frequeny_score(x):
    if x <= 3:
        return x
    else:
        return 4
    
RFM_table['R_score'] = RFM_table['recency'].apply(lambda x: assign_R_score(x, 'recency'))
RFM_table['M_score'] = RFM_table['monetary'].apply(lambda x: assign_M_score(x, 'monetary'))
RFM_table['F_score'] = RFM_table['frequency'].apply(cust_frequeny_score)
RFM_table['Total_RFM_score'] = RFM_table[['R_score', 'M_score', 'F_score']].sum(axis=1)
RFM_table['RFM_group'] = RFM_table['R_score'].astype(str) + RFM_table['M_score'].astype(str) + RFM_table['F_score'].astype(str)

def assign_segments(x):
    if x <= 5:
        return 'low valued customers'
    elif x <= 9: 
        return 'medium valued customers'
    else:
        return 'high valued customers'

RFM_table['segments'] = RFM_table['Total_RFM_score'].apply(lambda x: assign_segments(x))

    
    