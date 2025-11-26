import os
import base64
import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CID Tracker", layout="wide")
st.title("CID Tracker")

# ---------- Storage settings ----------
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

# Load existing data (for persistence across runs)
if os.path.exists(DATA_FILE):
    df_data = pd.read_csv(DATA_FILE)
else:
    df_data = pd.DataFrame(columns=COLUMNS)

# ---------- GitHub config ----------
GITHUB_OWNER = "Nikhil-Lakha"
GITHUB_REPO = "cidTracker"
GITHUB_BRANCH = "main"
GITHUB_FILE_PATH = "cid_trackers.csv"
GITHUB_API_BASE = "https://api.github.com"


def push_csv_to_github(csv_path: str, tracking_code: str) -> None:
    """Upload / update cid_trackers.csv in the GitHub repo."""
    token = st.secrets.get("GITHUB_TOKEN")
    if not token:
        st.warning("GitHub token not configured in secrets; skipping GitHub upload.")
        return

    url = f"{GITHUB_API_BASE}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    # 1. Get existing file SHA (if file already exists)
    sha = None
    r_get = requests.get(url, headers=headers)
    if r_get.status_code == 200:
        try:
            sha = r_get.json().get("sha")
        except Exception:
            sha = None
    elif r_get.status_code not in (200, 404):
        st.error(f"GitHub GET error {r_get.status_code}: {r_get.text}")
        return

    # 2. Read CSV and base64 encode it
    with open(csv_path, "rb") as f:
        content_bytes = f.read()
    content_b64 = base64.b64encode(content_bytes).decode("utf-8")

    payload = {
        "message": f"Update trackers – {tracking_code}",
        "content": content_b64,
        "branch": GITHUB_BRANCH,
    }
    if sha:
        payload["sha"] = sha

    # 3. PUT to GitHub
    r_put = requests.put(url, headers=headers, json=payload)
    if r_put.status_code not in (200, 201):
        st.error(f"GitHub PUT error {r_put.status_code}: {r_put.text}")
    else:
        st.success("cid_trackers.csv pushed to GitHub ✅")


# ---------------- Channel → Campaign Type ----------------
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

# ---------------- Business Unit → Product ----------------
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

# ---------------- Channel → Short code ----------------
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
    if channel in channel_code_map:
        return channel_code_map[channel]
    if channel:
        return channel[:2].upper()
    return "XX"


def build_tracking_link(target_url: str, cid_value: str) -> str:
    if not target_url:
        return ""
    sep = "&" if "?" in target_url else "?"
    return f"{target_url}{sep}cid={cid_value}"


# ---------------- UI Tabs ----------------
tab1, tab2, tab3 = st.tabs(["Create", "Trackers", "Video Tutorial"])

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

    # Row 1
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        campaign_name = st.text_input("Campaign Name")
    with r1c2:
        channel = st.selectbox("Channel", channel_options, index=0)

    # Campaign Type depends on channel
    campaign_type_options = [""]
    if channel in campaign_type_map:
        campaign_type_options += campaign_type_map[channel]

    # Row 2
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        campaign_type = st.selectbox("Campaign Type", campaign_type_options, index=0)
    with r2c2:
        campaign_objective = st.selectbox(
            "Campaign Objective", campaign_objective_options, index=0
        )

    # Row 3
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        start_date = st.date_input("Start Date")
    with r3c2:
        end_date = st.date_input("End Date")

    # Row 4
    r4c1, r4c2 = st.columns(2)
    with r4c1:
        business_unit = st.selectbox("Business Unit", business_unit_options, index=0)

    business_product_options = [""]
    if business_unit in business_product_map:
        business_product_options += business_product_map[business_unit]

    with r4c2:
        business_product = st.selectbox(
            "Business Product", business_product_options, index=0
        )

    # Row 5
    r5c1, r5c2 = st.columns(2)
    with r5c1:
        campaign_owner = st.text_input("Campaign Owner")
    with r5c2:
        target_url = st.text_input("Target URL")

    submitted = st.button("Save Campaign")

    if submitted:
        # ----- validation -----
        missing = []

        if not campaign_name.strip():
            missing.append("Campaign Name")
        if channel == "":
            missing.append("Channel")
        if campaign_type == "":
            missing.append("Campaign Type")
        if campaign_objective == "":
            missing.append("Campaign Objective")
        if not start_date:
            missing.append("Start Date")
        if not end_date:
            missing.append("End Date")
        if business_unit == "":
            missing.append("Business Unit")
        if business_product == "":
            missing.append("Business Product")
        if not campaign_owner.strip():
            missing.append("Campaign Owner")

        if not target_url.strip():
            missing.append("Target URL")
        else:
            url_lower = target_url.strip().lower()
            if "vodacom" not in url_lower and "vodapay" not in url_lower:
                missing.append("Target URL (must contain 'vodacom' or 'vodapay')")

        if missing:
            st.error(
                "Please fix the following before generating a tracking link:\n\n"
                + "• " + "\n• ".join(missing)
            )
        else:
            # ----- Generate CID + link -----
            next_number = BASE_CID_NUMBER + len(df_data)
            channel_code = get_channel_code(channel)
            tracking_code = f"{channel_code}_{next_number}"
            tracking_link = build_tracking_link(target_url, tracking_code)

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

            # Update local CSV
            df_data = pd.concat([df_data, pd.DataFrame([new_row])], ignore_index=True)
            df_data.to_csv(DATA_FILE, index=False)

            # Push CSV to GitHub
            push_csv_to_github(DATA_FILE, tracking_code)

            st.success("Campaign saved ✅")
            st.markdown("### Generated Tracking")
            st.write(f"**Tracking Code:** `{tracking_code}`")
            st.code(tracking_link or "", language="text")

            st.markdown("### Preview of Saved Data")
            st.write(new_row)

with tab2:
    st.markdown("### Trackers")
    if not df_data.empty:
        st.dataframe(df_data, use_container_width=True)
    else:
        st.info("No trackers created yet. Create one in the **Create** tab.")

with tab3:
    st.markdown("### Video Tutorial")
    st.info("A walkthrough video will appear here soon.")
