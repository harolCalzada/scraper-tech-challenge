from dataclasses import dataclass
from typing import Optional

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
    price: float
    similarity_score: float = 0.0  # Score to determine how well it matches the search criteria
    min_similarity_score: float = 0.6  # Minimum score to consider a match
    
    @property
    def found_match(self) -> bool:
        """Indicates if this product is considered a valid match based on similarity score."""
        return self.similarity_score >= self.min_similarity_score
