import streamlit as st

# Set the page configuration to use the full width
st.set_page_config(layout="wide")

# Set the headline
st.title("Marketing CID Tracker")

# Create tabs
tab1, tab2 = st.tabs(["Tracker", "List"])

with tab1:
    st.header("Tracker")
    
    # Ask users to choose the number of links
    num_links = st.number_input("How many links do you want to create?", min_value=1, max_value=10, value=1)
    
    # Create input fields for each link
    for i in range(num_links):
        st.subheader(f"Link {i+1}")
        campaign_name = st.text_input(f"Campaign Name {i+1}")
        channel = st.text_input(f"Channel {i+1}")
        campaign_type = st.text_input(f"Campaign Type {i+1}")
        campaign_objective = st.text_input(f"Campaign Objective {i+1}")
        business_unit = st.text_input(f"Business Unit {i+1}")
        business_product = st.text_input(f"Business Product {i+1}")
        start_date = st.date_input(f"Start Date {i+1}")
        end_date = st.date_input(f"End Date {i+1}")
        campaign_owner = st.text_input(f"Campaign Owner {i+1}")
        target_url = st.text_input(f"Target URL {i+1}")

with tab2:
    st.header("List")
    st.write("This is where you can list all your marketing CIDs.")
