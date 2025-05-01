from abc import ABC, abstractmethod
from typing import List
from ..entities.product import Product, ScrapedProduct

class ScraperPort(ABC):
    """Port defining the contract for web scrapers."""
    
    @abstractmethod
    async def search_product(self, product: Product) -> List[ScrapedProduct]:
        """
        Search for a product in the e-commerce platform.
        
        Args:
            product: Product entity containing search criteria
            
        Returns:
            List of ScrapedProduct entities found matching the criteria
        """
        pass
