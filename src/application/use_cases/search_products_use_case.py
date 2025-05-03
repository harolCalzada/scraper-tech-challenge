from typing import List, Union
from ...domain.ports.scraper_port import ScraperPort
from ...domain.ports.repository_port import ProductRepositoryPort
from ...domain.entities.product import Product, ScrapedProduct
from ...domain.services.product_matcher import ProductMatcher
import logging

logger = logging.getLogger(__name__)

class SearchProductsUseCase:
    """Application use case for searching products across e-commerce platforms."""
    
    def __init__(self, scrapers: Union[ScraperPort, List[ScraperPort]], repository: ProductRepositoryPort):
        # Convert single scraper to list if needed
        self.scrapers = [scrapers] if not isinstance(scrapers, list) else scrapers
        self.repository = repository
        self.product_matcher = ProductMatcher()
    
    async def execute(self, input_file: str, output_file: str) -> List[ScrapedProduct]:
        """
        Execute the product search workflow across multiple scrapers.
        
        Args:
            input_file: Path to input Excel file
            output_file: Path where to save results
            
        Returns:
            List of ScrapedProduct entities found
        """
        # Load products from Excel
        products = self.repository.load_products(input_file)
        
        # Search each product across all scrapers
        all_results = []
        for product in products:
            for scraper in self.scrapers:
                try:
                    results = await scraper.search_product(product)
                    
                    # Calculate similarity scores and filter matches
                    for result in results:
                        if self.product_matcher.is_match(product, result):
                            logger.info(f"Match found: {result.name} (score: {result.similarity_score})")
                            all_results.append(result)
                        else:
                            logger.debug(f"No match: {result.name} (score: {result.similarity_score})")
                            
                except Exception as e:
                    logger.error(f"Error with {scraper.__class__.__name__} for product {product.product_name}: {str(e)}", exc_info=True)
                    continue
        
        # Save results
        self.repository.save_results(output_file, all_results)
        
        return all_results
