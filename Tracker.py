import streamlit as st

# Set the headline
st.title("Marketing CID Tracker")

# Create tabs
tab1, tab2 = st.tabs(["Tracker", "List"])

with tab1:
    st.header("Tracker")
    st.write("This is where you can track your marketing CIDs.")

with tab2:
    st.header("List")
    st.write("This is where you can list all your marketing CIDs.")
