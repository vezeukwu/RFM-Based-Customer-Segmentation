import streamlit as st
import pickle
# from src.preprocessing import preprocess_input
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# page configuration
st.set_page_config(page_title="RoyalBank RFM Dashboard", layout="wide")

#load data with cache
@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\Admin\Desktop\DataScience 10alytics\Machine Learning\RFM-Based Customer Segmentation\Output\RFM_Segmented.csv")

df = load_data()

# --- Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Average Recency", f"{df['recency'].mean():.0f} days")
col2.metric("Average Frequency", f"{df['frequency'].mean():.1f}")
col3.metric("Average Monetary", f"${df['monetary'].mean():,.0f}")

st.markdown("---")

# --- Segment Distribution ---
segment_counts = df['Segment'].value_counts().reset_index()
segment_counts.columns = ['Segment', 'Count']

col4, col5 = st.columns(2)

with col4:
    st.subheader("📊 Customers by Segment")
    fig_bar = px.bar(segment_counts, x='Segment', y='Count', color='Segment',
                     color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_bar, use_container_width=True)

with col5:
    st.subheader("🧩 Segment Proportions")
    fig_pie = px.pie(segment_counts, names='Segment', values='Count',
                     color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- Filter and Bar Chart View ---
st.subheader("🔍 Explore Customers by Segment")
segment_filter = st.multiselect("Filter by Segment", options=df['Segment'].unique(), default=df['Segment'].unique())
filtered_df = df[df['Segment'].isin(segment_filter)]

# Bar Chart for Segment Distribution
segment_counts = filtered_df['Segment'].value_counts()

# Adjusting figure size
fig, ax = plt.subplots(figsize=(2, 2))  # Width: 2 inches, Height: 2 inches

# Plotting the bar chart
segment_counts.plot(kind='bar', ax=ax, color='skyblue')

# Customizing font sizes
ax.set_title("Customer Distribution by Segment", fontsize=6)
ax.set_xlabel("Segment", fontsize=3)
ax.set_ylabel("Number of Customers", fontsize=4)
ax.tick_params(axis='x', labelsize=3)  # X-axis labels
ax.tick_params(axis='y', labelsize=3)  # Y-axis labels

# Display the plot
st.pyplot(fig)

ax.set_xlabel("Recency")
ax.set_ylabel("Monetary")
ax.set_title("Recency vs Monetary by Segment", fontsize=6)
ax.legend(title="Segment", fontsize=2)
st.pyplot(fig)


st.dataframe(filtered_df)

# --- Download Button ---
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

csv = convert_df_to_csv(filtered_df)
st.download_button("📥 Download Filtered Data as CSV", data=csv, file_name="filtered_rfm_data.csv", mime='text/csv')