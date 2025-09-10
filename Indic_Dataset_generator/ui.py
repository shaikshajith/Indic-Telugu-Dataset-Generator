# ui.py
import streamlit as st
import pandas as pd
from scraper import scrape_and_collect, topic_sites  # import scraping function and topic dictionary

st.set_page_config(page_title="Telugu Dataset Scraper", layout="wide")
st.title("📌 Telugu News Dataset Generator")

# -------------------------------
# ✅ Sidebar for topic & subtopic selection
# -------------------------------
st.sidebar.header("Select Topic & Subtopic")
topic = st.sidebar.selectbox("Topic:", options=list(topic_sites.keys()))
subtopic = st.sidebar.selectbox("Subtopic:", options=list(topic_sites[topic].keys()))

# -------------------------------
# ✅ Filename input
# -------------------------------
filename = st.text_input("Enter filename (without extension):", value="telugu_dataset")

# -------------------------------
# ✅ Scrape & Save button
# -------------------------------
if st.button("Scrape & Save Dataset"):
    with st.spinner(f"Scraping {topic} - {subtopic}..."):
        df = scrape_and_collect(topic, subtopic)
        if not df.empty:
            st.success(f"✅ Scraping done! {len(df)} articles collected.")
            st.dataframe(df.head(10))  # preview first 10 rows

            # Save CSV
            csv_file = f"{filename}.csv"
            df.to_csv(csv_file, index=False, encoding="utf-8-sig")
            st.download_button(
                label="📥 Download CSV",
                data=open(csv_file, "rb").read(),
                file_name=csv_file,
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No Telugu text found for this selection.")
