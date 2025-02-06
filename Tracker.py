import streamlit as st
import pandas as pd

# Define the initial dataframe with your specified columns
df = pd.DataFrame(
    [
       {
           "Campaign Name": "Summer Sale",
           "Channel": "Facebook",
           "Campaign Type": "Paid",
           "Campaign Objective": "Brand Awareness",
           "Business Unit": "Retail",
           "Business Product": "Shoes",
           "Start Date": "2024-06-01",
           "End Date": "2024-06-30",
           "Campaign Owner": "John Doe",
           "Target URL": "https://example.com/summer-sale",
           "CID Campaign Link": "cid123"
       },
       {
           "Campaign Name": "Winter Deals",
           "Channel": "Google Ads",
           "Campaign Type": "Paid",
           "Campaign Objective": "Conversions",
           "Business Unit": "E-commerce",
           "Business Product": "Jackets",
           "Start Date": "2024-07-01",
           "End Date": "2024-07-31",
           "Campaign Owner": "Jane Smith",
           "Target URL": "https://example.com/winter-deals",
           "CID Campaign Link": "cid456"
       }
   ]
)

# Create an editable data editor with dynamic row addition
edited_df = st.data_editor(df, num_rows="dynamic")

# Identify the campaign with the latest start date as the most recent campaign
most_recent_campaign = edited_df.loc[edited_df["Start Date"].idxmax()]["Campaign Name"]
st.markdown(f"Your most recent campaign is **{most_recent_campaign}** 🚀")
