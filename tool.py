import streamlit as st
from extra_streamlit_components import CookieManager
import os, random, pandas as pd
# from pydub import AudioSegment
from datetime import datetime 
import re
import plotly.express as px

# --- User Authentication and RBAC ---
import streamlit_authenticator as stauth

# Define credentials dictionary for streamlit-authenticator >=0.4.2
credentials = {
    "usernames": {
        "amanda.bio-marfo@nationwidemh.com": {
            "name": "Amanda Bio-Marfo",
            "password": stauth.Hasher.hash("123")
        },
        "suraiyatu.mohammed@nationwidemh.com": {
            "name": "Surayatu Mohammed",
            "password": stauth.Hasher.hash("456")
        },
        "edem.dzitrie@nationwidemh.com": {
            "name": "Edem Dzitrie",
            "password": stauth.Hasher.hash("789")
        }
    }
}

cookie_manager = CookieManager(key="qa_app_tool_cookie_manager")

authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="qa_app_tool",
    key="qa_app_tool_auth",
    expiry_days=1,
    cookie_manager=cookie_manager
)

# Login widget
authenticator.login(location='main')

# Get values from session state
name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

def get_user_role(username):
    # Example static mapping; replace with DB lookup as needed
    role_map = {
        "amanda.bio-marfo@nationwidemh.com": "admin",
        "suraiyatu.mohammed@nationwidemh.com": "auditor",
        "edem.dzitrie@nationwidemh.com": "supervisor"
    }
    return role_map.get(username, None)

def show_admin_panel():
    st.info("Admin Panel: You have full access.")

def show_approval_dashboard():
    st.info("Supervisor Dashboard: You have full access.")

def show_audit_form():
    st.info("Auditor Form: You have full access.")

if authentication_status:
    st.success(f"Welcome {name}")
    user_role = get_user_role(username)
    if user_role == "admin":
        show_admin_panel()
    elif user_role == "supervisor":
        show_approval_dashboard()
    elif user_role == "auditor":
        show_audit_form()
    
    # --- Place the rest of the dashboard code below this block ---
else:
    if authentication_status == False:
        st.error("Invalid credentials")
    else:
        st.warning("Enter login details")
    st.stop()

st.image("logos\\logo.png", width=180)

st.set_page_config(page_title="QA Audio Call Selector", layout="wide")
st.title("🎧 QA Audio Call Selector")

# Initialize session state for uploaded files
if 'uploaded_files_folder' not in st.session_state:
    st.session_state.uploaded_files_folder = None

# Choose input method
input_method = st.radio("Choose input method:", ["📁 From Folder Path", "📤 Upload Files"], horizontal=True)

folder_path = None

if input_method == "📁 From Folder Path":
    # Folder input
    folder_path = st.text_input("📁 Enter or select folder path containing call recordings:")

else:  # Upload Files
    # File uploader
    st.write("**Upload recorded call files (MP3, WAV, M4A)**")
    uploaded_files = st.file_uploader(
        "Choose audio files to upload",
        type=["mp3", "wav", "m4a"],
        accept_multiple_files=True,
        key="call_file_uploader"
    )

    if uploaded_files:
        # Create temporary directory for uploaded files if not already created
        if st.session_state.uploaded_files_folder is None:
            import tempfile
            st.session_state.uploaded_files_folder = tempfile.mkdtemp()

        temp_dir = st.session_state.uploaded_files_folder

        # Save uploaded files
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
        folder_path = temp_dir
    else:
        st.info("No files uploaded yet. Please select audio files to proceed.")
        folder_path = None


if folder_path and os.path.isdir(folder_path):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith((".mp3", ".wav", ".m4a"))]

    if not files:
        st.warning("No audio files found in this folder.")
    else:
        st.success(f"Found {len(files)} recordings.")

        # Optional: extract agent name or date from filenames
        df = pd.DataFrame({"File_Name": files})

        # work from filename without extension
        df["Base"] = df["File_Name"].str.rsplit(".", n=1).str[0]

        # Agent: first segment before the first underscore
        df["Agent"] = df["Base"].str.split("_").str[0].str.strip("[]").fillna("Unknown").replace("", "Unknown")

        # extract date from the third segment (after second "_"), with common-format fallbacks
        def _extract_date_from_base(base):
            parts = base.split("_")
            seg = parts[2] if len(parts) > 2 else ""
            if not seg:
                return "Unknown"
            m = re.search(r"(\d{4}-\d{2}-\d{2})", seg)          # YYYY-MM-DD
            if m:
                return m.group(1)
            m = re.search(r"(\d{8})", seg)                    # YYYYMMDD
            if m:
                s = m.group(1)
                return f"{s[0:4]}-{s[4:6]}-{s[6:8]}"
            m = re.search(r"(\d{2}-\d{2}-\d{4})", seg)        # DD-MM-YYYY
            if m:
                d = m.group(1)
                day, month, year = d.split("-")
                return f"{year}-{month}-{day}"
            return "Unknown"

        df["Date"] = df["Base"].apply(_extract_date_from_base)
        df["Contact"] = df["File_Name"].apply(lambda x: os.path.join(folder_path, x))

        # Initialize all QA columns with exact names from audit report
        df["Id"] = range(1, len(df) + 1)
        df["Name"] = ""
        df["Date of interaction"] = df["Date"]
        df["AHT (seconds)"] = ""
        df["Agent"] = df["Name of Call Centre Officer"] = df["Agent"]
        df["Type of caller"] = ""
        df["Name of caller"] = ""
        df["Caller's phone number"] = ""
        df["Caller's organization/Name of facility"] = ""
        df["Language spoken"] = ""
        df["Purpose of call"] = ""
        df["Did CCO open the call using the appropriate greetings?"] = ""
        df["Was the CCO able to identify and verify the needs of the customer?"] = ""
        df["Was the CCO able to educate & inform the customer about the query/enquiry/request"] = ""
        df["Did the CCO ensure and confirm the necessary steps to query resolution?"] = ""
        df["Did the CCO accept responsibility for the query? (CAN DO)"] = ""
        df["Did the CCO speak clearly and fluently throughout the call?"] = ""
        df["Was the CCO professional?"] = ""
        df["Was the CCO able to communicate effectively through effective listening and troubleshooting?"] = ""
        df["Was the CCO polite & courteous?"] = ""
        df["Did the CCO show empathy? (introduce solution statement)"] = ""
        df["Did the CCO ask if you had any further needs?"] = ""
        df["Did the CCO end the call politely and professionally?"] = ""
        df["Total Score"] = 0
        df["Fatal"] = ""
        df["QA Score"] = 0.0
        df["Do you have any other comments you would like to share?"] = ""

        # Choose sampling type
        sampling_type = st.radio("🎯 Sampling Type", ["Pure Random", "Stratified by Agent"])
        sample_size = st.number_input("🔢 Number of Calls to Audit", min_value=1, value=5)

        if st.button("🎲 Select Random Calls"):
            selected = pd.DataFrame()

            if sampling_type == "Pure Random":
                selected = df.sample(n=min(sample_size, len(df)))

            elif sampling_type == "Stratified by Agent":
                agents = df["Agent"].unique()
                total_calls = len(df)
                samples_per_agent = {}
                total_allocated = 0
                for a in agents:
                    num = len(df[df["Agent"] == a])
                    proportion = num / total_calls if total_calls > 0 else 0
                    allocated = round(sample_size * proportion)
                    if allocated == 0 and num > 0:
                        allocated = 1
                    samples_per_agent[a] = min(allocated, num)
                    total_allocated += samples_per_agent[a]

                # If total allocated is less than sample_size, add more to agents with remaining capacity
                if total_allocated < sample_size:
                    remaining = sample_size - total_allocated
                    agents_sorted = sorted(agents, key=lambda a: len(df[df["Agent"] == a]) - samples_per_agent[a], reverse=True)
                    for a in agents_sorted:
                        can_add = len(df[df["Agent"] == a]) - samples_per_agent[a]
                        if can_add > 0:
                            add = min(remaining, can_add)
                            samples_per_agent[a] += add
                            remaining -= add
                            if remaining == 0:
                                break

                for a in agents:
                    subset = df[df["Agent"] == a]
                    selected = pd.concat([selected, subset.sample(n=samples_per_agent[a])])

            # Store selected in session state
            st.session_state.selected = selected.copy()

        # Display selections if available
        if 'selected' in st.session_state:
            selected = st.session_state.selected
            st.subheader("✅ Selected Calls for QA Audit")

            # Initialize session state for all fields if not present
            # Benchmark-aligned quality questions and their scores
            quality_questions = [
                ("Did CCO open the call using the appropriate greetings?", 3),
                ("Was the CCO able to identify and verify the needs of the customer?", 4),
                ("Was the CCO able to educate & inform the customer about the query/enquiry/request", 15),
                ("Did the CCO ensure and confirm the necessary steps to query resolution?", 5),
                ("Did the CCO accept responsibility for the query? (CAN DO)", 5),
                ("Did the CCO speak clearly and fluently throughout the call?", 5),
                ("Was the CCO professional?", 15),
                ("Was the CCO able to communicate effectively through effective listening and troubleshooting?", 15),
                ("Was the CCO polite & courteous?", 10),
                ("Did the CCO show empathy? (introduce solution statement)", 15),
                ("Did the CCO ask if you had any further needs?", 5),
                ("Did the CCO end the call politely and professionally?", 3)
            ]



            for i in selected.index:
                # Metadata fields
                if f"name_{i}" not in st.session_state:
                    st.session_state[f"name_{i}"] = selected.at[i, 'Name'] if selected.at[i, 'Name'] else ''
                if f"aht_{i}" not in st.session_state:
                    st.session_state[f"aht_{i}"] = selected.at[i, 'AHT (seconds)'] if selected.at[i, 'AHT (seconds)'] else ''
                if f"caller_type_{i}" not in st.session_state:
                    st.session_state[f"caller_type_{i}"] = selected.at[i, 'Type of caller'] if selected.at[i, 'Type of caller'] else ''
                if f"caller_name_{i}" not in st.session_state:
                    st.session_state[f"caller_name_{i}"] = selected.at[i, 'Name of caller'] if selected.at[i, 'Name of caller'] else ''
                if f"cc_officer's_name_{i}" not in st.session_state:
                    st.session_state[f"cc_officer's_name_{i}"] = selected.at[i, 'Name of Call Centre Officer'] if selected.at[i, 'Name of Call Centre Officer'] else ''
                if f"caller_phone_{i}" not in st.session_state:
                    st.session_state[f"caller_phone_{i}"] = selected.at[i, "Caller's phone number"] if selected.at[i, "Caller's phone number"] else ''
                if f"caller_org_{i}" not in st.session_state:
                    st.session_state[f"caller_org_{i}"] = selected.at[i, "Caller's organization/Name of facility"] if selected.at[i, "Caller's organization/Name of facility"] else ''
                if f"language_{i}" not in st.session_state:
                    st.session_state[f"language_{i}"] = selected.at[i, 'Language spoken'] if selected.at[i, 'Language spoken'] else ''
                if f"purpose_{i}" not in st.session_state:
                    st.session_state[f"purpose_{i}"] = selected.at[i, 'Purpose of call'] if selected.at[i, 'Purpose of call'] else ''

                # Quality metrics
                for q, _ in quality_questions:
                    if f"{q}_{i}" not in st.session_state:
                        st.session_state[f"{q}_{i}"] = selected.at[i, q] if q in selected.columns and selected.at[i, q] else ''

                # Other fields
                if f"fatal_{i}" not in st.session_state:
                    st.session_state[f"fatal_{i}"] = selected.at[i, 'Fatal'] if selected.at[i, 'Fatal'] else ''
                if f"comments_{i}" not in st.session_state:
                    st.session_state[f"comments_{i}"] = selected.at[i, 'Do you have any other comments you would like to share?'] if selected.at[i, 'Do you have any other comments you would like to share?'] else ''

            # Collect widget values
            form_data = {}
            for i, row in selected.iterrows():
                st.write(f"## 🎙️ Call {i+1}: {row['File_Name']}")
                st.write(f"**Agent:** {row['Agent']} | **Date:** {row['Date']}")
                st.audio(row["Contact"])

                # Cancel button for Not Applicable (N/A)
                if st.button(f"Cancel (N/A) for Call {i+1}", key=f"cancel_na_{i}"):
                    st.session_state[f"na_{i}"] = True
                if f"na_{i}" in st.session_state and st.session_state[f"na_{i}"]:
                    st.info("This call has been marked as Not Applicable (N/A) and will be skipped.")
                    form_data[f"na_{i}"] = True
                    st.divider()
                    continue
                else:
                    form_data[f"na_{i}"] = False

                with st.expander("📋 Call Metadata & Caller Info", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        form_data[f"name_{i}"] = st.text_input(f"Auditor's Name", value=st.session_state[f"name_{i}"], key=f"name_input_{i}")
                        form_data[f"aht_{i}"] = st.number_input(f"AHT (seconds)", value=int(st.session_state[f"aht_{i}"]) if st.session_state[f"aht_{i}"] else 0, key=f"aht_input_{i}")
                        form_data[f"cc_officer's_name_{i}"] = st.text_input(f"CC Officer's Name", value=st.session_state[f"cc_officer's_name_{i}"], key=f"cc_officer_name_input_{i}")
                        form_data[f"caller_name_{i}"] = st.text_input(f"Caller Name", value=st.session_state[f"caller_name_{i}"], key=f"caller_name_input_{i}")
                    with col2:
                        form_data[f"caller_phone_{i}"] = st.text_input(f"Caller Phone", value=st.session_state[f"caller_phone_{i}"], key=f"caller_phone_input_{i}")
                        form_data[f"caller_org_{i}"] = st.text_input(f"Caller Organization", value=st.session_state[f"caller_org_{i}"], key=f"caller_org_input_{i}")
                        form_data[f"language_{i}"] = st.selectbox(f"Language Spoken", ["", "English", "Twi", "Ga", "Other"], index=["", "English", "Twi", "Ga", "Other"].index(st.session_state[f"language_{i}"] if st.session_state[f"language_{i}"] else ""), key=f"language_input_{i}")
                        form_data[f"purpose_{i}"] = st.selectbox(f"Purpose of Call", ["", "Complaint", "Enquiry", "Request"], index=["", "Complaint", "Enquiry", "Request"].index(st.session_state[f"purpose_{i}"] if st.session_state[f"purpose_{i}"] else ""), key=f"purpose_input_{i}")

                with st.expander("⭐ Quality Metrics (Rate as Yes/No)", expanded=True):
                    col1, col2 = st.columns(2)
                    for idx, (q, score) in enumerate(quality_questions):
                        label = f"{q} (Score: {score})"
                        if q == "Was the CCO able to identify and verify the needs of the customer?":
                            options = ["", "0", "3", "4", "NA"]
                        elif q == "Was the CCO able to educate & inform the customer about the query/enquiry/request":
                            options = ["", "0", "5", "10", "13", "15", "Fatal"]
                        elif q == "Did the CCO ensure and confirm the necessary steps to query resolution?":
                            options = ["", "0", "4", "5", "NA"]
                        elif q == "Did the CCO accept responsibility for the query? (CAN DO)":
                            options = ["", "0", "2", "5", "NA"]
                        elif q == "Did the CCO speak clearly and fluently throughout the call?":
                            options = ["", "0", "2", "5"]
                        elif q == "Was the CCO professional?":
                            options = ["", "0", "3", "6", "9", "12", "15"]
                        elif q == "Was the CCO able to communicate effectively through effective listening and troubleshooting?":
                            options = ["", "0", "5", "10", "14", "15"]
                        elif q == "Was the CCO polite & courteous?":
                            options = ["", "0", "5", "10", "Fatal"]
                        elif q == "Did the CCO show empathy? (introduce solution statement)":
                            options = ["", "0", "10", "13", "14", "15", "NA"]
                        else:
                            options = ["", "0", "1", "2", "3", "NA"]
                        idx_default = options.index(str(st.session_state[f"{q}_{i}"]) if st.session_state[f"{q}_{i}"] else "")
                        if idx % 2 == 0:
                            form_data[f"{q}_{i}"] = col1.selectbox(label, options, index=idx_default, key=f"{q}_input_{i}")
                        else:
                            form_data[f"{q}_{i}"] = col2.selectbox(label, options, index=idx_default, key=f"{q}_input_{i}")

                with st.expander("📝 Additional Info", expanded=False):
                    form_data[f"comments_{i}"] = st.text_area(f"Comments", value=st.session_state[f"comments_{i}"], key=f"comments_input_{i}")

                st.divider()

            # Save audit log button
            if st.button("💾 Save Audit Log"):

                # Update selected from form data
                selected_save = st.session_state.selected.copy()

                for i in selected_save.index:
                    # If marked as N/A, set a flag and skip scoring/inputs
                    if form_data.get(f"na_{i}", False):
                        selected_save.at[i, 'Not Applicable'] = 'N/A'
                        selected_save.at[i, 'Total Score'] = 0
                        selected_save.at[i, 'QA Score'] = 0.0
                        selected_save.at[i, 'Do you have any other comments you would like to share?'] = form_data.get(f"comments_{i}", '')
                        continue

                    # Metadata
                    selected_save.at[i, 'Name'] = form_data.get(f"name_{i}", '')
                    selected_save.at[i, 'AHT (seconds)'] = form_data.get(f"aht_{i}", '')
                    selected_save.at[i, 'Type of caller'] = form_data.get(f"caller_type_{i}", '')
                    selected_save.at[i, 'Name of caller'] = form_data.get(f"caller_name_{i}", '')
                    selected_save.at[i, "Caller's phone number"] = form_data.get(f"caller_phone_{i}", '')
                    selected_save.at[i, "Caller's organization/Name of facility"] = form_data.get(f"caller_org_{i}", '')
                    selected_save.at[i, 'Language spoken'] = form_data.get(f"language_{i}", '')
                    selected_save.at[i, 'Purpose of call'] = form_data.get(f"purpose_{i}", '')

                    # Quality metrics
                    total_score = 0
                    for q, score in quality_questions:
                        answer = form_data.get(f"{q}_{i}", '')
                        selected_save.at[i, q] = answer
                        if answer == "Yes":
                            total_score += score

                    # Other fields
                    selected_save.at[i, 'Do you have any other comments you would like to share?'] = form_data.get(f"comments_{i}", '')

                    # Compute Total Score and QA Score
                    selected_save.at[i, 'Total Score'] = total_score
                    selected_save.at[i, 'QA Score'] = (total_score / 100) if total_score > 0 else 0.0

                # Show current working directory for debugging
                st.info(f"Current working directory: {os.getcwd()}")
                st.write("Data to be saved:")
                st.dataframe(selected_save)

                try:
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    selected_save["Audit_Timestamp"] = timestamp
                    filename = f"audit_log_{timestamp}.xlsx"
                    selected_save.to_excel(filename, index=False)
                    st.success(f"Audit selections saved successfully! File: {filename}")
                except Exception as e:
                    st.error(f"Failed to save audit log: {e}")

                # Optional: display summary
                st.write("**Audit Summary:**")
                st.dataframe(selected_save[["Agent", "File_Name", "Date", "Total Score", "Do you have any other comments you would like to share?"]])

                # QA Statistics
                st.write("**QA Statistics:**")
                if not selected_save.empty and selected_save['Total Score'].notna().any():
                    avg_score = selected_save['Total Score'].mean()
                    st.write(f"Overall Average Total Score: {avg_score:.2f} / 100")
                    # Ensure all columns are string type before groupby
                    stats_df = selected_save.copy()
                    stats_df['Agent'] = stats_df['Agent'].astype(str)
                    stats_df['Total Score'] = stats_df['Total Score'].astype(int)
                    agent_stats = stats_df.groupby('Agent')['Total Score'].agg(['mean', 'count']).reset_index()
                    agent_stats = agent_stats.rename(columns={'mean': 'Average Score', 'count': 'Call Count'})
                    st.write("Average Score and Call Count by Agent:")
                    st.dataframe(agent_stats)
                    # Bar chart
                    fig = px.bar(
                        agent_stats,
                        x='Agent',
                        y='Average Score',
                        title='Average Total Score by Agent',
                        labels={'Average Score': 'Average Score', 'Agent': 'Agent Name'},
                        color='Average Score',
                        color_continuous_scale='RdYlGn',
                        range_color=[0, 100]
                    )
                    fig.update_layout(
                        font=dict(family="Arial, sans-serif", size=14),
                        title_font=dict(family="Arial, sans-serif", size=18, color="#222"),
                        xaxis_title_font=dict(family="Arial, sans-serif", size=16),
                        yaxis_title_font=dict(family="Arial, sans-serif", size=16)
                    )
                    st.plotly_chart(fig)
                else:
                    st.write("No QA scores available for statistics.")
                st.write(f"Total Comments Provided: {selected_save['Do you have any other comments you would like to share?'].str.strip().ne('').sum()}")
