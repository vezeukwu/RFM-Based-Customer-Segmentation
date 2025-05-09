from src.rfm_eda import compute_rfm
from src.clustering import perform_clustering
from utils import load_data, save_data


def main():
    #Load cleaned data
    df = load_data('C:\Users\Admin\Desktop\DataScience 10alytics\Machine Learning\RFM-Based Customer Segmentation\Output\Cleaned_df.csv')
    
    #step 1: RFM Calculation
    RFM_table = compute_rfm(df)
    
    #step 2: Clustering
    clustered = perform_clustering(RFM_table)

    #save final dataset
    save_data(clustered, 'output/rfm_segmented.csv')
    print(' RFM segmentation completed and saved to output/RFM_segmented.csv' )
    
#if_"name_": "_main_":
#main()