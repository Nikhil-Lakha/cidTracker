import streamlit as st
import pandas as pd

# Define an empty dataframe with the required columns
columns = [
    "Campaign Name", "Channel", "Campaign Type", "Campaign Objective",
    "Business Unit", "Business Product", "Start Date", "End Date",
    "Campaign Owner", "Target URL", "CID Campaign Link"
]
df = pd.DataFrame(columns=columns)

# Create an editable data editor with dynamic row addition
edited_df = st.data_editor(df, num_rows="dynamic")

# Display a message if data is entered
if not edited_df.empty:
    most_recent_campaign = edited_df.loc[edited_df["Start Date"].idxmax()]["Campaign Name"]
    st.markdown(f"Your most recent campaign is **{most_recent_campaign}** 🚀")
