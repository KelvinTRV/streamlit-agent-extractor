import re
import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Streamlit UI
st.title("Insurance Agent Data Extractor")
st.write("Enter a webpage URL or upload an HTML file to extract agent details.")

# User input for URL
url = st.text_input("Enter the webpage URL:")

# File uploader (optional)
uploaded_file = st.file_uploader("Or upload an HTML file", type=["txt", "html"])

# Function to fetch HTML from a URL
def fetch_html(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            return response.text
        else:
            st.error(f"Failed to retrieve page (Status code: {response.status_code})")
            return None
    except Exception as e:
        st.error(f"Error fetching URL: {e}")
        return None

# Get HTML data (either from URL or uploaded file)
raw_data = None
if url:
    raw_data = fetch_html(url)
elif uploaded_file:
    raw_data = uploaded_file.read().decode("utf-8")

if raw_data:
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(raw_data, "html.parser")
    html_text = str(soup)  # Convert to string for regex parsing

    # Define regex patterns
    agent_pattern = re.compile(r'data-key="([^"]+)"')
    title_pattern = re.compile(r'class="[^"]*nameSubHeader">([^<]+)<')
    phone_pattern = re.compile(r'href="tel:([^"]+)"')
    email_pattern = re.compile(r'href="mailto:([^"]+)"')
    rating_pattern = re.compile(r'ratingNumber">([^<]+)</span>')
    reviews_pattern = re.compile(r'count">\((\d+) Reviews\)</span>')

    # Extract data
    agents = agent_pattern.findall(html_text)
    titles = title_pattern.findall(html_text)
    phones = phone_pattern.findall(html_text)
    emails = email_pattern.findall(html_text)
    ratings = rating_pattern.findall(html_text)
    reviews = reviews_pattern.findall(html_text)

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

    st.success("Extraction complete! ✅")
