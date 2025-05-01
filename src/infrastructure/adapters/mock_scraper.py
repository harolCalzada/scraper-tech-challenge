from typing import List
from ...domain.ports.scraper_port import ScraperPort
from ...domain.entities.product import Product, ScrapedProduct
from ..config.settings import app_settings

class MockScraper(ScraperPort):
    """Mock implementation of scraper for testing."""
    
    async def search_product(self, product: Product) -> List[ScrapedProduct]:
        """Return mock data for testing."""
        # Create a mock result
        mock_result = ScrapedProduct(
            source_sku=product.product_sku,
            marketplace="mock-store",
            name=f"Mock {product.product_name}",
            url="https://mock-store.com/product-123",
            price=99.99,
            similarity_score=0.8
        )
        
        return [mock_result]
