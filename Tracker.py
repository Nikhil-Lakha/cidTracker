import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CID Tracker", layout="wide")

st.title("CID Tracker")

# --------- Storage settings ---------
# Always save in the same folder as this script (your repo folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "cid_trackers.csv")
BASE_CID_NUMBER = 200000

COLUMNS = [
    "Campaign Name",
    "Channel",
    "Campaign Type",
    "Campaign Objective",
    "Business Unit",
    "Business Product",
    "Start Date",
    "End Date",
    "Campaign Owner",
    "Target URL",
    "Tracking Code",
    "Tracking Link",
]

# Load existing data (for persistence across sessions)
if os.path.exists(DATA_FILE):
    df_data = pd.read_csv(DATA_FILE)
else:
    df_data = pd.DataFrame(columns=COLUMNS)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Create", "Trackers", "Video Tutorial"])


# -----------------------------------------------
# CHANNEL → CAMPAIGN TYPE MAPPING
# -----------------------------------------------
campaign_type_map = {
    "Display": [
        "Native ads",
        "Video",
        "Remarketing Ads",
        "Gmail Sponsored Promotions",
        "Standard Display",
        "Smart Display",
        "Rich Media",
        "Discovery",
        "HTML",
        "GIF",
    ],
    "eBill": ["Banner", "Email", "SMS", "MMS"],
    "Email": ["Email Banner", "Email CTA", "In-Page links"],
    "Magazine": ["Product CTA", "Service CTA"],
    "Mobile": ["Rich Media", "SMS", "USSD", "Push Notifications"],
    "Affilliates": ["Banner", "Email", "MMS", "SMS", "Social", "QR"],
    "Paid Search": ["Google Search", "Google Shopping", "Text Ads"],
    "Social Media": [
        "Facebook: Organic",
        "Facebook: Paid",
        "Facebook: Shopping",
        "Instagram: Organic",
        "Instagram: Paid",
        "Instagram: Shopping",
        "Tik Tok: Organic",
        "Tik Tok: Paid",
        "Twitter: Organic",
        "Twitter: Paid",
        "Video",
        "GIF",
        "Carousel Static",
        "Carousel Video",
        "Collection",
        "Story Video",
        "Story Static",
        "LinkedIn",
    ],
    "Sponsorship": ["Banner", "Email", "MMS", "SMS", "Social"],
    "Youtube Owned Channel": ["Video", "Description"],
    "Retail": ["Display", "Till Slip", "Boxes", "Brochure", "Screens"],
    "Blog": ["Banner", "In-page link"],
}

# -----------------------------------------------
# BUSINESS UNIT → BUSINESS PRODUCT MAPPING
# -----------------------------------------------
business_product_map = {
    "Lending": [
        "Business Term Advance",
        "Business Cash Advance",
        "Voucher Advance",
        "Cash Advance",
        "Airtime advance",
        "Compare",
        "Trade Advance",
        "Personal Loans",
        "DLS Streamy",
    ],
    "Insurance": [
        "Device Insurance",
        "Funeral Cover",
        "Life Cover",
        "Legal Assist",
        "Medi-Assist",
        "Hero Assist",
        "RoadSave",
        "Roadside Assist",
    ],
    "POS": [
        "Payment Solutions",
        "Vodacom Ordering Solutions",
        "Vodapay Max",
        "Vodapay Kwika",
        "Vodapay Chop-Chop",
        "Activation Portal",
        "Merchant Portal",
        "VodaPay e-commerce",
        "VodaPay Tap on Phone",
        "VodaPay Payment request.",
    ],
    "VodaTrade": ["VodaTrade: All"],
    "DLS Music": ["My Muze"],
    "DLS Gaming": ["PlayInc"],
    "DLS Streamy": [],
}

business_unit_options = [
    "",
    "Lending",
    "Insurance",
    "POS",
    "VodaTrade",
    "DLS Music",
    "DLS Gaming",
    "DLS Streamy",
]

campaign_objective_options = [
    "",
    "Revenue Generation",
    "Lead Generation",
    "Awareness",
]

# -----------------------------------------------
# CHANNEL → SHORT CODE FOR CID
# -----------------------------------------------
channel_code_map = {
    "Social Media": "SM",
    "Email": "EM",
    "Display": "DS",
    "Paid Search": "PS",
    "Affilliates": "AF",
    "eBill": "EB",
    "Magazine": "MG",
    "Mobile": "MO",
    "Sponsorship": "SP",
    "Youtube Owned Channel": "YT",
    "Retail": "RT",
    "Blog": "BL",
    "Video": "VD",
    "Staff Screensaver": "SS",
}


def get_channel_code(channel: str) -> str:
    """Return 2–3 letter code for channel, default to first 2 letters if not mapped."""
    if channel in channel_code_map:
        return channel_code_map[channel]
    if channel:
        return channel[:2].upper()
    return "XX"


def build_tracking_link(target_url: str, cid_value: str) -> str:
    """Append cid param to the target URL, handling existing query params."""
    if not target_url:
        return ""
    sep = "&" if "?" in target_url else "?"
    return f"{target_url}{sep}cid={cid_value}"


# -----------------------------------------------
# TAB 1: CREATE
# -----------------------------------------------
with tab1:
    st.markdown("### Enter Campaign Details")

    channel_options = [
        "",
        "Affilliates",
        "Blog",
        "Display",
        "eBill",
        "Email",
        "Magazine",
        "Mobile",
        "Paid Search",
        "Social Media",
        "Sponsorship",
        "Youtube Owned Channel",
        "Video",
        "Retail",
        "Staff Screensaver",
    ]

    # ---------- ROW 1 ----------
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        campaign_name = st.text_input("Campaign Name")
    with row1_col2:
        channel = st.selectbox("Channel", channel_options, index=0)

    # Build campaign type options after channel is chosen
    campaign_type_options = [""]
    if channel in campaign_type_map:
        campaign_type_options += campaign_type_map[channel]

    # ---------- ROW 2 ----------
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        campaign_type = st.selectbox(
            "Campaign Type",
            campaign_type_options,
            index=0,
            help="Options depend on the selected Channel.",
        )
    with row2_col2:
        campaign_objective = st.selectbox(
            "Campaign Objective",
            campaign_objective_options,
            index=0,
        )

    # ---------- ROW 3 ----------
    row3_col1, row3_col2 = st.columns(2)
    with row3_col1:
        start_date = st.date_input("Start Date")
    with row3_col2:
        end_date = st.date_input("End Date")

    # ---------- ROW 4 ----------
    row4_col1, row4_col2 = st.columns(2)
    with row4_col1:
        business_unit = st.selectbox(
            "Business Unit",
            business_unit_options,
            index=0,
        )

    business_product_options = [""]
    if business_unit in business_product_map:
        business_product_options += business_product_map[business_unit]

    with row4_col2:
        business_product = st.selectbox(
            "Business Product",
            business_product_options,
            index=0,
        )

    # ---------- ROW 5 ----------
    row5_col1, row5_col2 = st.columns(2)
    with row5_col1:
        campaign_owner = st.text_input("Campaign Owner")
    with row5_col2:
        target_url = st.text_input("Target URL")

    submitted = st.button("Save Campaign")

    tracking_link = ""
    tracking_code = ""

    if submitted:
        # ---- Validation ----
        missing_fields = []

        if not campaign_name.strip():
            missing_fields.append("Campaign Name")
        if channel == "":
            missing_fields.append("Channel")
        if campaign_type == "":
            missing_fields.append("Campaign Type")
        if campaign_objective == "":
            missing_fields.append("Campaign Objective")
        if not start_date:
            missing_fields.append("Start Date")
        if not end_date:
            missing_fields.append("End Date")
        if business_unit == "":
            missing_fields.append("Business Unit")
        if business_product == "":
            missing_fields.append("Business Product")
        if not campaign_owner.strip():
            missing_fields.append("Campaign Owner")

        # Target URL validation
        if not target_url.strip():
            missing_fields.append("Target URL")
        else:
            url_lower = target_url.strip().lower()
            if not ("vodacom" in url_lower or "vodapay" in url_lower):
                missing_fields.append(
                    "Target URL (must contain 'vodacom' or 'vodapay')"
                )

        if missing_fields:
            st.error(
                "Please fix the following before generating a tracking link:\n\n"
                + "• " + "\n• ".join(missing_fields)
            )
        else:
            # --- Determine next number based on existing rows in file ---
            next_number = BASE_CID_NUMBER + len(df_data)

            channel_code = get_channel_code(channel)
            tracking_code = f"{channel_code}_{next_number}"

            tracking_link = build_tracking_link(target_url, tracking_code)

            # Build new row
            new_row = {
                "Campaign Name": campaign_name,
                "Channel": channel,
                "Campaign Type": campaign_type,
                "Campaign Objective": campaign_objective,
                "Business Unit": business_unit,
                "Business Product": business_product,
                "Start Date": start_date,
                "End Date": end_date,
                "Campaign Owner": campaign_owner,
                "Target URL": target_url,
                "Tracking Code": tracking_code,
                "Tracking Link": tracking_link,
            }

            # Append to dataframe and save to CSV (in repo folder)
            df_data = pd.concat([df_data, pd.DataFrame([new_row])], ignore_index=True)
            df_data.to_csv(DATA_FILE, index=False)

            st.success("Campaign saved ✅")

            st.markdown("### Generated Tracking")
            st.write(f"**Tracking Code:** `{tracking_code}`")
            st.write("**Tracking Link:**")
            if tracking_link:
                st.code(tracking_link, language="text")
            else:
                st.warning(
                    "No Target URL provided, so tracking link could not be generated."
                )

            st.markdown("### Preview of Saved Data")
            st.write(new_row)

# -----------------------------------------------
# TAB 2: TRACKERS
# -----------------------------------------------
with tab2:
    st.markdown("### Trackers")

    if not df_data.empty:
        st.dataframe(df_data, use_container_width=True)
    else:
        st.info("No trackers created yet. Create one in the **Create** tab.")

# -----------------------------------------------
# TAB 3: VIDEO TUTORIAL
# -----------------------------------------------
with tab3:
    st.markdown("### Video Tutorial")
    st.info("A walkthrough video will appear here soon.")
