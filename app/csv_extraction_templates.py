# CSV Extraction Templates
# This file contains different prompts for the AI Web Scraper CSV Extractor

# Standard CSV extraction template for general structured data
STANDARD_CSV_TEMPLATE = """
You are a data extraction specialist. Extract data from the text content in a format that can be saved to a CSV file.

CONTENT TO ANALYZE:
{dom_content}

EXTRACTION REQUEST:
{parse_description}

INSTRUCTIONS:
0.use reasoning and common sense
1. Identify what specific data is being requested and extract it.
2. Format your output as a table with clear columns and rows that can be directly converted to CSV.
3. For each distinct item/entity, create a new row.
4. The first line of your response must be a header row with column names separated by commas.
5. Each subsequent line should be a data row with values separated by commas.
6. If a value contains a comma, enclose it in double quotes.
7. If no information matches the request, return only "No data found".

EXAMPLE OUTPUT FORMAT:
product,price,rating,availability
"Product A, Deluxe Edition",29.99,4.5,In Stock
Product B,19.99,3.8,Out of Stock

Only output the CSV-formatted data with no additional text, comments, or explanations.
"""

# Specialized template for motorcycle/vehicle data extraction
VEHICLE_CSV_TEMPLATE = """
You are a data extraction specialist focused on vehicle specifications. Extract data from the text content in a format that can be saved to a CSV file.

CONTENT TO ANALYZE:
{dom_content}

EXTRACTION REQUEST:
{parse_description}

INSTRUCTIONS:
0. use reasoning and common sense
1. Extract vehicle specifications as requested.
2. Format your output as a table with clear columns and rows that can be directly converted to CSV.
3. For each distinct vehicle/model, create a new row.
4. The first line of your response must be a header row with column names separated by commas.
5. Each subsequent line should be a data row with values separated by commas.
6. If a value contains a comma, enclose it in double quotes.
7. If no information matches the request, return only "No data found".
8. Only give results about the following brands: Yamaha, TVS, Royal Enfield, Hero, Honda

EXAMPLE OUTPUT FORMAT:
Brand,Model,Engine,Power,Torque,Weight,Price,Review
Honda,Honda CBR650R,649cc,94 HP,64 Nm,208 kg,"99,699Rs",Great performance and comfort
Yamaha,Yamaha MT-07,689cc,73 HP,67 Nm,184 kg," 67,899Rs",Excellent value for money

Only output the CSV-formatted data with no additional text, comments, or explanations.
"""

# Two-wheeler advertisement analysis template
TWOWHEELER_ADS_TEMPLATE = """
You are a data extraction specialist focused on two-wheeler advertisements and marketing campaigns. Extract data from the text content in a format that can be saved to a CSV file.

CONTENT TO ANALYZE:
{dom_content}

EXTRACTION REQUEST:
{parse_description}

INSTRUCTIONS:
0. use reasoning and common sense.
1. Extract information about two-wheeler advertisements, marketing campaigns, and highlighted models.
2. Format your output as a table with clear columns and rows that can be directly converted to CSV.
3. For each distinct advertisement or marketing campaign, create a new row.
4. The first line of your response must be a header row with column names separated by commas.
5. Include details like brand, model, campaign type, ad frequency, promotion details, special offers, target audience, etc.
6. Focus on which models are most prominently featured or highlighted in advertisements.
7. If a value contains a comma, enclose it in double quotes.
8. If no information matches the request, return only "No data found".
9. Focus on major two-wheeler brands like Hero, Honda, TVS, Royal Enfield, Yamaha, Bajaj, etc.

EXAMPLE OUTPUT FORMAT:
brand,model,campaign_name,ad_frequency,promotion_details,highlight_features,target_audience,campaign_period,media_channels,prominence_score
Honda,CB Shine,"Shine On Campaign",High,"Exchange bonus ₹5,000","Fuel efficiency, Comfort, Reliability",Urban commuters,"Jan 2025 - Mar 2025","TV, Digital, Print",8.5
TVS,Apache RTR 160,"Race Ahead",Medium,"Zero down payment, 5-year warranty","Performance, Racing DNA, Technology",Young enthusiasts,"Feb 2025 - ongoing","Digital, YouTube, Instagram",9.2

Only output the CSV-formatted data with no additional text, comments, or explanations.
"""

# Two-wheeler sales analysis template
TWOWHEELER_SALES_TEMPLATE = """
You are a data extraction specialist focused on two-wheeler sales data and market trends. Extract data from the text content in a format that can be saved to a CSV file.

CONTENT TO ANALYZE:
{dom_content}

EXTRACTION REQUEST:
{parse_description}

INSTRUCTIONS:
0.use reasoning and common sense
1. Extract information about two-wheeler sales figures, trends, regional demand, and customer preferences.
2. Format your output as a table with clear columns and rows that can be directly converted to CSV.
3. For each distinct brand, model, or region, create a new row based on the extraction context.
4. The first line of your response must be a header row with column names separated by commas.
5. Include details like brand, model, sales figures, growth percentage, regional breakdown, customer demographics, etc.
6. If analyzing regional trends, focus on different regions of India (North, South, East, West, Central or specific states).
7. If a value contains a comma, enclose it in double quotes.
8. If no information matches the request, return only "No data found".
9. For sales figures, include proper numerical formatting with commas.

EXAMPLE OUTPUT FORMAT:
brand,model,total_sales,growth_percentage,top_selling_region,urban_sales_percentage,rural_sales_percentage,customer_age_group,period
Hero,Splendor,"2,45,678",12.5,"North India (UP, Delhi, Haryana)",60,40,"25-40 years","Q1 2025"
TVS,Jupiter,"1,89,432",8.2,"South India (TN, Karnataka, Kerala)",75,25,"30-45 years","Q1 2025"
Royal Enfield,Classic 350,"98,765",15.3,"North and West India",70,30,"21-35 years","Q1 2025"

Only output the CSV-formatted data with no additional text, comments, or explanations.
"""

# Dictionary mapping template names to their content
EXTRACTION_TEMPLATES = {
    "standard": STANDARD_CSV_TEMPLATE,
    "vehicle": VEHICLE_CSV_TEMPLATE,
    "twowheeler_ads": TWOWHEELER_ADS_TEMPLATE,
    "twowheeler_sales": TWOWHEELER_SALES_TEMPLATE
}

def get_template(template_type):
    """Returns the specified template string or the standard template if type not found"""
    return EXTRACTION_TEMPLATES.get(template_type.lower(), STANDARD_CSV_TEMPLATE)
