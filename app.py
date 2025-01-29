import re
import pandas as pd
import streamlit as st

# Streamlit UI
st.title("Insurance Agent Data Extractor")
st.write("Upload a raw HTML file to extract agent details.")

# File uploader
uploaded_file = st.file_uploader("Upload HTML file", type=["txt", "html"])

if uploaded_file:
    # Read file content
    raw_data = uploaded_file.read().decode("utf-8")

    # Define regex patterns
    agent_pattern = re.compile(r'data-key="([^"]+)"')
    title_pattern = re.compile(r'class="[^"]*nameSubHeader">([^<]+)<')
    phone_pattern = re.compile(r'href="tel:([^"]+)"')
    email_pattern = re.compile(r'href="mailto:([^"]+)"')
    rating_pattern = re.compile(r'ratingNumber">([^<]+)</span>')
    reviews_pattern = re.compile(r'count">\((\d+) Reviews\)</span>')

    # Extract data
    agents = agent_pattern.findall(raw_data)
    titles = title_pattern.findall(raw_data)
    phones = phone_pattern.findall(raw_data)
    emails = email_pattern.findall(raw_data)
    ratings = rating_pattern.findall(raw_data)
    reviews = reviews_pattern.findall(raw_data)

    # Ensure correct alignment
    data = list(zip(agents, titles, phones, emails, ratings, reviews))

    # Create DataFrame
    df = pd.DataFrame(data, columns=["Agent Name", "Title", "Phone Number", "Email Address", "Star Rating", "Reviews"])

    # Show extracted data
    st.subheader("Extracted Agent Data")
    st.dataframe(df)

    # Convert to CSV
    csv = df.to_csv(index=False).encode("utf-8")

    # Provide download button
    st.download_button("Download CSV", csv, "agent_data.csv", "text/csv")

    st.success("Extraction complete! Download the CSV file above. ✅")
