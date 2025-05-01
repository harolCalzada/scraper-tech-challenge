from typing import List
from difflib import SequenceMatcher
from ...domain.entities.product import Product, ScrapedProduct

class ProductMatcherService:
    """Service for matching products based on similarity."""
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """Calculate similarity ratio between two strings."""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def match_products(self, source_product: Product, scraped_products: List[ScrapedProduct],
                      min_similarity: float = 0.6) -> List[ScrapedProduct]:
        """
        Match scraped products against source product using various criteria.
        
        Args:
            source_product: Original product to match against
            scraped_products: List of products found through scraping
            min_similarity: Minimum similarity ratio to consider a match
            
        Returns:
            List of matched products sorted by similarity score
        """
        for scraped_product in scraped_products:
            # Ensure source SKU is set
            scraped_product.source_sku = source_product.product_sku
            
            # Calculate base similarity from product name
            name_similarity = self.calculate_similarity(
                source_product.product_name,
                scraped_product.title
            )
            
            # Weight different matching criteria
            weights = {
                'name': 0.5,
                'category': 0.2,
                'brand': 0.3
            }
            
            # Calculate category match
            category_match = any(
                cat.lower() in scraped_product.title.lower()
                for cat in [source_product.category, source_product.subcategory, 
                           source_product.sub_subcategory]
            )
            
            # Calculate brand/line match
            brand_match = any(
                brand.lower() in scraped_product.title.lower()
                for brand in [source_product.product_line, source_product.product_group]
            )
            
            # Calculate final similarity score
            scraped_product.similarity_score = (
                name_similarity * weights['name'] +
                (weights['category'] if category_match else 0) +
                (weights['brand'] if brand_match else 0)
            )
        
        # Sort by similarity score in descending order
        return sorted(scraped_products, key=lambda x: x.similarity_score, reverse=True)
