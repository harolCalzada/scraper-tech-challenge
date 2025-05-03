from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class Product:
    """Domain entity representing a product from the input Excel file."""
    product_sku: str
    product_name: str
    product_line: str
    product_group: str
    category: str
    subcategory: str
    sub_subcategory: str
    area: str
    status: str

@dataclass
class ScrapedProduct:
    """Domain entity representing a product found through web scraping."""
    # Source product information
    source_sku: str  # SKU from the input Excel
    marketplace: str  # 'walmart' or 'mercadolibre'
    
    # Scraped product information
    name: str
    url: str
    price: float  # Current price (with discount if applicable)
    original_price: float = 0.0  # Original price before discount
    discount_percentage: float = 0.0  # Discount percentage if applicable
    similarity_score: float = 0.0  # Score to determine how well it matches the search criteria
    min_similarity_score: float = 0.2  # Minimum score to consider a match
    
    # Additional product details
    destination_sku: str = ''  # SKU found in the product description
    ean: str = ''  # EAN/UPC code if available
    brand: str = ''  # Product brand
    model: str = ''  # Product model
    color: str = ''  # Product color
    specifications: dict = None  # Additional specifications (material, dimensions, etc)
    categories: list = None  # Product categories from breadcrumb navigation
    
    @property
    def found_match(self) -> bool:
        """Indicates if this product is considered a valid match based on similarity score."""
        logger.info(f"Similarity score: {self.similarity_score} for product {self.name}")
        return self.similarity_score >= self.min_similarity_score
