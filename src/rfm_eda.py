# Importing relevant libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Loading the data
df = pd.read_csv(R"C:\Users\Admin\Desktop\DataScience 10alytics\Machine Learning\RFM-Based Customer Segmentation\Data\bank_data_C.csv")

# Converting the date columns to date-time formats
df["CustomerDOB"] = pd.to_datetime(df["CustomerDOB"], errors='coerce')
df["TransactionDate"] = pd.to_datetime(df["TransactionDate"], errors='coerce')

# Cleaning the DOB column by locating the columns with wrong DOBs and substracting 100years from it.
df.loc[df["CustomerDOB"].dt.year > 1999, "CustomerDOB"] = df["CustomerDOB"] - pd.DateOffset(years=100)

# Calculating the mean of DOB excluding 1800
df.loc[df["CustomerDOB"].dt.year > 1800, "CustomerDOB"].mean()
# Replacing the outliers in date with the mean of the dates

# Defining the replacement timestampvenv\Scripts\activate

replacement_date = pd.Timestamp('1985-05-16 00:02:25.560537728')
# Replace dates in CustomerDOB with year 1800
df.loc[df["CustomerDOB"].dt.year == 1800, "CustomerDOB"] = replacement_date


# dropping the rows with transaction amount of 0
df.drop(df[df["TransactionAmount (INR)"] == 0].index.tolist(), axis =0, inplace = True)

# Locations with the highest number of customers
top_custlocation = df.groupby('CustLocation')['CustomerID'].nunique().sort_values(ascending= False)
plt.figure(figsize=(10,6))
top_custlocation.head(10).plot(kind='bar', color='skyblue')
plt.xlabel('Customer Location')
plt.ylabel('Number of Customers')
plt.title('Locations with the highest number of Customers')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

df.groupby('Month').size().plot(kind='line')
plt.xlabel('Transaction Month')
plt.ylabel('Transaction Volume')
plt.title('Monthly Transaction Trend')
#plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

# Save cleaned data
df.to_csv("Cleaned_df.csv", index=False)

