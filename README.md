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

- Python 3.9 or higher
- Git

## Installation

### Core Installation (For Production Use)

```bash
# Clone the repository
git clone https://github.com/harolCalzada/scraper-tech-challenge.git
cd scraper-tech-challenge

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

# Install core dependencies
pip install -r requirements.txt
```

### Development Installation

If you want to contribute to the project or run the Jupyter notebooks locally:

```bash
# After following the core installation steps above
pip install -r requirements-dev.txt
```

### Google Colab Usage

To use the scraper in Google Colab:

1. Open the notebook in `notebooks/product_scraper_colab_demo.ipynb`
2. The notebook will automatically install the required dependencies
3. Follow the instructions in the notebook

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/harolCalzada/scraper-tech-challenge.git
   cd scraper-tech-challenge
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

1. Start Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

2. In your browser, navigate to the `notebooks` directory

3. Open `product_scraper_demo.ipynb`

4. You can now run the cells in the notebook

### Stopping the Project

1. To stop Jupyter Notebook: Press `Ctrl+C` in the terminal
2. To deactivate the virtual environment:
   ```bash
   deactivate
   ```

## Usage

### Using the Jupyter Notebook

1. Place your input Excel file in the `input` directory as `products.xlsx`
2. Open and run the Jupyter notebook `notebooks/product_scraper_demo.ipynb`
3. The results will be saved in the `output` directory as `results.xlsx`

The notebook provides an interactive environment where you can:

- View the processing steps
- Inspect intermediate results
- Modify parameters if needed
- See detailed error messages if they occur

## Production Demo

Colab demo: [link](https://colab.research.google.com/drive/1GhiF7jlEHnTO5s1qO7k3dje4NUDDOcDW?usp=sharing)

## Project Structure

```
├── notebooks/          # Jupyter notebooks
│   └── product_scraper_demo.ipynb
├── src/                # Source code
│   ├── domain/         # Domain layer
│   │   ├── entities/   # Domain entities
│   │   └── ports/      # Interface definitions
│   ├── application/    # Application layer
│   │   ├── services/   # Domain services
│   │   └── use_cases/  # Application use cases
│   └── infrastructure/ # Infrastructure layer
│       ├── adapters/   # Concrete implementations
│       └── config/     # Configuration
├── input/              # Input Excel files
├── output/             # Generated results
└── requirements.txt    # Project dependencies
```

## Notes

- The script is well-documented and includes comments for better understanding
- Designed to run locally with clear execution instructions
- Implements error handling and retry mechanisms
