import streamlit as st
import os, random, pandas as pd
# from pydub import AudioSegment
from datetime import datetime

st.set_page_config(page_title="QA Audio Call Selector", layout="wide")
st.title("🎧 QA Audio Call Selector")

# Folder input
folder_path = st.text_input("📁 Enter or select folder path containing call recordings:")

if folder_path and os.path.isdir(folder_path):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith((".mp3", ".wav", ".m4a"))]

    if not files:
        st.warning("No audio files found in this folder.")
    else:
        st.success(f"Found {len(files)} recordings.")

        # Extract agent name or date from filenames
        df = pd.DataFrame({"File_Name": files})
        df["Agent"] = df["File_Name"].str.extract(r"([A-Za-z]+)")  # simple pattern example
        df["Date"] = df["File_Name"].str.extract(r"(\d{4}-\d{2}-\d{2})")
        df["Contact"] = df["File_Name"].apply(lambda x: os.path.join(folder_path, x))

        # Choose sampling type
        sampling_type = st.radio("🎯 Sampling Type", ["Pure Random", "Stratified by Agent"])
        sample_size = st.number_input("🔢 Number of Calls to Audit", min_value=1, value=5)

        if st.button("🎲 Select Random Calls"):
            selected = pd.DataFrame()

            if sampling_type == "Pure Random":
                selected = df.sample(n=min(sample_size, len(df)))

            elif sampling_type == "Stratified by Agent":
                agents = df["Agent"].dropna().unique()
                per_agent = max(1, sample_size // len(agents))
                for a in agents:
                    subset = df[df["Agent"] == a]
                    selected = pd.concat([selected, subset.sample(n=min(per_agent, len(subset)))])
                selected = selected.sample(n=min(sample_size, len(selected)))

            # Display selections
            st.subheader("✅ Selected Calls for QA Audit")
            for i, row in selected.iterrows():
                st.write(f"🎙️ **{row['File_Name']}** (Agent: {row['Agent']}, Call_Date: {row['Call_Date']})")
                st.audio(row["Contact"])

            # Save audit log
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            selected["Audit_Timestamp"] = timestamp
            selected.to_excel(f"audit_log_{timestamp}.xlsx", index=False)
            st.success("Audit selections saved successfully!")

            # Display summary
            st.write("**Audit Summary:**")
            st.dataframe(selected[["Agent", "File_Name", "Call_Date" ]])
            
