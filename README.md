# E-commerce Product Scraper

## Project Overview
This Python-based web scraper is designed to search and extract product information from major e-commerce platforms (walmart.com.mx or mercadolibre.com.mx) based on an input Excel file containing product details.

## Objectives
- Develop a Python script that searches products on e-commerce platforms using Excel file input
- Match and extract relevant product information
- Export results in a structured format

## Features
- Excel file input processing
- Automated product search on e-commerce platforms
- Intelligent product matching
- Data extraction for matched products:
  - Unique identifier code
  - Product title
  - Current sale price
  - List price (without discount)
  - Product URL
  - Seller name
  - Product image URL

## Input Format
The script expects an Excel file with the following columns:
- SKU
- Product Name
- Brand/Supplier
- Category

## Output Format
Results are exported to Excel/CSV with the following structure:
- Product
- Found Title
- Price
- URL
- Seller
- Image

## Technical Requirements
- Python 3.x
- Required libraries:
  - requests/BeautifulSoup/Selenium (for web scraping)
  - pandas (for Excel handling)
  - Additional dependencies listed in `requirements.txt`

## Installation
1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Place your input Excel file in the project directory
2. Run the script:
   ```bash
   python scraper.py
   ```
3. Find the results in the output Excel/CSV file

## Project Structure
```
├── scraper.py           # Main script
├── requirements.txt     # Project dependencies
├── input/              # Input Excel files
└── output/             # Generated results
```

## Notes
- The script is well-documented and includes comments for better understanding
- Designed to run locally with clear execution instructions
- Implements error handling and retry mechanisms
