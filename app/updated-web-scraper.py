import os
import streamlit as st
import logging
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import RemoteConnection
from bs4 import BeautifulSoup
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import re
import streamlit_nested_layout

# Import extraction templates
from csv_extraction_templates import get_template, EXTRACTION_TEMPLATES

# Load environment variables
load_dotenv()
SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Path for CSV storage
CSV_DIR = r"C:\Users\sanka\Documents\web_Scrapper"
if not os.path.exists(CSV_DIR):
    os.makedirs(CSV_DIR)

def scrape_website(website):
    """Launches a remote browser session and scrapes the website."""
    logging.info("Connecting to Scraping Browser...")

    sbr_connection = RemoteConnection(SBR_WEBDRIVER, keep_alive=True)

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    try:
        with webdriver.Remote(command_executor=sbr_connection, options=chrome_options) as driver:
            driver.get(website)
            logging.info("Navigated! Scraping page content...")
            html = driver.page_source
            return html if html else ""
    except Exception as e:
        logging.error("Error during web scraping: %s", str(e))
        return ""

def extract_body_content(html_content):
    """Extracts the <body> content from HTML."""
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    return str(soup.body) if soup.body else ""

def clean_body_content(body_content):
    """Removes script and style tags and returns cleaned text."""
    if not body_content:
        return ""
    soup = BeautifulSoup(body_content, "html.parser")
    for tag in soup(["script", "style"]):
        tag.extract()
    cleaned_content = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

def split_dom_content(dom_content, max_length=6000):
    """Splits the content into chunks of max_length."""
    if not dom_content:
        return []
    return [dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)]

# LLM model setup
model = Ollama(
    model="llama3",
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=0.25
)


def parse_with_ollama_for_csv(dom_chunks, parse_description, template_type):
    """Uses Ollama LLM to parse content specifically for CSV output."""
    if not dom_chunks:
        return "No relevant content found."
    
    # Get the appropriate template based on user selection
    template_string = get_template(template_type)
    prompt = ChatPromptTemplate.from_template(template_string)
    chain = prompt | model
    
    all_results = []
    for chunk in dom_chunks:
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
        all_results.append(response)
    
    combined_response = "\n".join(all_results)
    
    # Clean up the response to ensure it's properly formatted for CSV
    lines = combined_response.strip().split('\n')
    
    # If we have multiple headers (from multiple chunks), keep only the first one
    if len(lines) > 2:
        headers = lines[0]
        data_rows = []
        
        # Process each line, skipping any repeated headers
        for line in lines[1:]:
            # Skip empty lines
            if not line.strip():
                continue
            # Skip lines that match the header pattern
            if line == headers:
                continue
            # Add data rows
            data_rows.append(line)
        
        return headers + '\n' + '\n'.join(data_rows)
    
    return combined_response

def save_to_csv(parsed_result, url, parse_description, template_type):
    """Saves extracted data into a CSV file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scraped_data_{timestamp}.csv"
    csv_path = os.path.join(CSV_DIR, filename)
    
    # Extract data from the parsed result
    lines = parsed_result.strip().split('\n')
    
    if not lines or lines[0] == "No data found":
        # Create a CSV with just metadata if no data was found
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "URL", "Query", "Template", "Result"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                url,
                parse_description,
                template_type,
                "No data found"
            ])
    else:
        # Write the extracted data directly to CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            file.write(parsed_result)
        
        # Add metadata to a separate CSV file
        metadata_path = os.path.join(CSV_DIR, f"metadata_{timestamp}.csv")
        with open(metadata_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "URL", "Query", "Template"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                url,
                parse_description,
                template_type
            ])
    
    return csv_path

def preview_csv_as_dataframe(csv_content):
    """Converts CSV content string to a pandas DataFrame for display."""
    lines = csv_content.strip().split('\n')
    if not lines or lines[0] == "No data found":
        return pd.DataFrame({"Message": ["No data found"]})
    
    try:
        # Use StringIO to parse the CSV content directly
        import io
        df = pd.read_csv(io.StringIO(csv_content))
        return df
    except Exception as e:
        logging.error(f"Error converting CSV to DataFrame: {str(e)}")
        # Fallback manual parsing
        try:
            headers = lines[0].split(',')
            data = []
            for line in lines[1:]:
                # Handle quoted values with commas inside them
                values = []
                in_quotes = False
                current_value = ""
                for char in line:
                    if char == '"' and not in_quotes:
                        in_quotes = True
                    elif char == '"' and in_quotes:
                        in_quotes = False
                    elif char == ',' and not in_quotes:
                        values.append(current_value)
                        current_value = ""
                    else:
                        current_value += char
                values.append(current_value)  # Add the last value
                data.append(values)
            
            return pd.DataFrame(data, columns=headers)
        except:
            return pd.DataFrame({"Error": ["Could not parse CSV format"]})

# Streamlit UI

st.title("AI Web Scraper & Extractor")
st.markdown("Extract structured data from websites save it")

url = st.text_input("Enter Website URL", placeholder="https://example.com")

# Step 1: Scrape the Website
if st.button("Scrape Website", type="primary"):
    if url:
        with st.status("Scraping website...", expanded=True) as status:
            st.write(f"Connecting to {url}...")
            dom_content = scrape_website(url)
            if not dom_content:
                status.update(label="Scraping failed", state="error")
                st.error("Failed to scrape the website. Please check the URL or try again.")
            else:
                st.write("Extracting and cleaning content...")
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)
                st.session_state.dom_content = cleaned_content
                st.session_state.current_url = url
                status.update(label="Website scraped successfully!", state="complete")
                
                with st.expander("Preview scraped content"):
                    st.text_area("Raw content sample (first 1000 chars)", 
                                cleaned_content[:1000] + ("..." if len(cleaned_content) > 1000 else ""), 
                                height=200)

# Step 2: Extract Information for CSV
if "dom_content" in st.session_state and st.session_state.dom_content:
    st.divider()
    st.subheader("Extract Information ")
    
    # Template selection
    template_options = {
        "Standard": "standard",
        "Vehicle/Motorcycle Data": "vehicle",
        "twowheeler_ads": "Example: Extract current marketing campaigns by Honda and Yamaha, focusing on which models are being heavily advertised this month",
        "twowheeler_sales": "Example: Extract sales figures for Royal Enfield models across different regions of India in the last quarter"
    }
    
    template_col, info_col = st.columns([1, 3])
    
    with template_col:
        template_type = st.selectbox(
            "Select Extraction Template:", 
            options=list(template_options.keys()),
            format_func=lambda x: x,
            index=0
        )
    
    with info_col:
        template_key = template_options[template_type]
        if template_key == "standard":
            st.info("General purpose data extraction for any type of content.")
        elif template_key == "vehicle":
            st.info(" for vehicle data")
        
        elif  template_key == "twowheeler_ads":
           st.info("💡 This template works best on news sites, manufacturer websites, and marketing campaign pages.")
        elif template_key == "twowheeler_sales":
          st.info("💡 This template works best on industry reports, sales statistics pages, and financial news articles.")
    
    parse_description = st.text_area(
        "What information do you want to extract?",
        placeholder="Example: Extract all motorcycles with their specifications including model, engine size, power, torque, weight and price",
        height=100
    )
    
    if st.button("Extract Data ", type="primary"):
        if parse_description:
            selected_template = template_options[template_type]
            
            with st.status("Processing...", expanded=True) as status:
                st.write("Analyzing content...")
                dom_chunks = split_dom_content(st.session_state.dom_content)
                
                st.write(f"Extracting data with AI using {template_type} template...")
                parsed_result = parse_with_ollama_for_csv(dom_chunks, parse_description, selected_template)
                
                st.write("Saving data as CSV...")
                csv_file = save_to_csv(parsed_result, st.session_state.current_url, parse_description, selected_template)
                
                status.update(label="Data extracted successfully!", state="complete")
            
            # Preview the data as a table
            st.subheader("Extracted Data Preview")
            df = preview_csv_as_dataframe(parsed_result)
            st.dataframe(df)
            
            # Provide download link
            csv_filename = os.path.basename(csv_file)
            with open(csv_file, "rb") as file:
                st.download_button(
                    label=f"📥 Download  ({csv_filename})",
                    data=file,
                    file_name=csv_filename,
                    mime="text/csv"
                )

# Add footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #888;">
    AI Web Scraper •  Data Extraction Tool
</div>
""", unsafe_allow_html=True)
