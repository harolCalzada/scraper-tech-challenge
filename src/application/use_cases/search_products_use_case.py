from typing import List
from ...domain.ports.scraper_port import ScraperPort
from ...domain.ports.repository_port import ProductRepositoryPort
from ...domain.entities.product import Product, ScrapedProduct

class SearchProductsUseCase:
    """Application use case for searching products across e-commerce platforms."""
    
    def __init__(self, scraper: ScraperPort, repository: ProductRepositoryPort):
        self.scraper = scraper
        self.repository = repository
    
    async def execute(self, input_file: str, output_file: str) -> List[ScrapedProduct]:
        """
        Execute the product search workflow.
        
        Args:
            input_file: Path to input Excel file
            output_file: Path where to save results
            
        Returns:
            List of ScrapedProduct entities found
        """
        # Load products from Excel
        products = self.repository.load_products(input_file)
        
        # Search each product
        all_results = []
        for product in products:
            results = await self.scraper.search_product(product)
            all_results.extend(results)
        
        # Save results
        self.repository.save_results(output_file, all_results)
        
        return all_results
