import asyncio
import logging
from infrastructure.adapters.walmart_scraper import WalmartScraper
from infrastructure.adapters.mercadolibre_scraper import MercadoLibreScraper
from infrastructure.adapters.excel_repository import ExcelRepository
from application.use_cases.search_products_use_case import SearchProductsUseCase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Initialize scrapers
        walmart_scraper = WalmartScraper()
        mercadolibre_scraper = MercadoLibreScraper()
        
        # Initialize repository
        repository = ExcelRepository()
        
        # Initialize use case with both scrapers
        use_case = SearchProductsUseCase(
            scrapers=[walmart_scraper, mercadolibre_scraper],
            repository=repository
        )
        
        # Execute search
        input_file = "input.xlsx"  # Update with your input file path
        output_file = "output.xlsx"  # Update with your output file path
        
        results = await use_case.execute(input_file, output_file)
        logger.info(f"Found {len(results)} total products across all marketplaces")
        
    except Exception as e:
        logger.error("Error in main execution", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main())
