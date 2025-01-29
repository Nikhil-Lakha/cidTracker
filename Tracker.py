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
    
    # Create input fields for each link in a horizontal layout
    for i in range(num_links):
        st.subheader(f"Link {i+1}")
        cols = st.columns(10)
        campaign_name = cols[0].text_input(f"Campaign Name {i+1}")
        channel = cols[1].text_input(f"Channel {i+1}")
        campaign_type = cols[2].text_input(f"Campaign Type {i+1}")
        campaign_objective = cols[3].text_input(f"Campaign Objective {i+1}")
        business_unit = cols[4].text_input(f"Business Unit {i+1}")
        business_product = cols[5].text_input(f"Business Product {i+1}")
        start_date = cols[6].date_input(f"Start Date {i+1}")
        end_date = cols[7].date_input(f"End Date {i+1}")
        campaign_owner = cols[8].text_input(f"Campaign Owner {i+1}")
        target_url = cols[9].text_input(f"Target URL {i+1}")

with tab2:
    st.header("List")
    st.write("This is where you can list all your marketing CIDs.")
