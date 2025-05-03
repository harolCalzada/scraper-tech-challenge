from typing import Dict
from dataclasses import dataclass

@dataclass
class ScraperSettings:
    """Configuration settings for scrapers."""
    user_agent: str
    request_delay: float
    max_retries: int
    timeout: int

@dataclass
class AppSettings:
    """Application-wide settings."""
    min_similarity_score: float = 0.6
    max_results_per_product: int = 5
    supported_sites: Dict[str, str] = None
    
    def __post_init__(self):
        if self.supported_sites is None:
            self.supported_sites = {
                'walmart': 'https://www.walmart.com.mx',
                'mercadolibre': 'https://listado.mercadolibre.com.mx'
            }

# Default scraper settings
default_scraper_settings = ScraperSettings(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    request_delay=3.0,  # Base delay between requests in seconds (will increase with exponential backoff)
    max_retries=8,      # Maximum number of retries per request
    timeout=45          # Increased timeout for slower connections
)

# Application settings
app_settings = AppSettings()
