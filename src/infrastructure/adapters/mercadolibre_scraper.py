import logging
import random
import time
import asyncio
import requests
import re
from bs4 import BeautifulSoup
from typing import List, Optional
from urllib.parse import urljoin, quote
from ...domain.ports.scraper_port import ScraperPort
from ...domain.entities.product import Product, ScrapedProduct
from ..config.settings import app_settings, default_scraper_settings

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add console handler if not already present
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n%(exc_info)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def log_error(msg: str, exc_info: Exception = None) -> None:
    """Helper function to log errors with full traceback."""
    if exc_info:
        logger.error(msg, exc_info=True)
    else:
        logger.error(msg)

class MercadoLibreScraper(ScraperPort):
    """Implementation of scraper for MercadoLibre Mexico."""
    
    def __init__(self):
        self.base_url = app_settings.supported_sites['mercadolibre']
        self.session = requests.Session()
        self._init_session()
        
    def _init_session(self) -> None:
        """Initialize a session with basic headers."""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-MX,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        })
    
    def _make_request(self, url: str, retries: int = None) -> Optional[requests.Response]:
        """Make HTTP request with retries."""
        if retries is None:
            retries = default_scraper_settings.max_retries
            
        for attempt in range(retries):
            try:
                # Add random delay between requests
                delay = random.uniform(1, 3) * (1.5 ** attempt)
                time.sleep(delay)
                
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response
                
            except Exception as e:
                logger.error(f"Request error on attempt {attempt + 1} for URL {url}", exc_info=True)
                if attempt == retries - 1:
                    return None
                time.sleep(random.uniform(2, 5))
    
    def _extract_price(self, price_text: str) -> float:
        """Extract price from text."""
        try:
            # Remove any non-numeric characters except dots and commas
            clean_text = ''.join(c for c in price_text if c.isdigit() or c in '.,').strip()
            
            # Handle different price formats
            if ',' in clean_text and '.' not in clean_text:
                # Format: "1,840" -> 1840.00
                clean_text = clean_text.replace(',', '') + '.00'
            elif '.' in clean_text and ',' not in clean_text:
                # Format: "1.840" -> 1840.00
                if len(clean_text.split('.')[-1]) <= 2:
                    # It's a decimal point
                    pass
                else:
                    # It's a thousands separator
                    clean_text = clean_text.replace('.', '') + '.00'
            elif ',' in clean_text and '.' in clean_text:
                # Format: "1,840.00" -> 1840.00
                clean_text = clean_text.replace(',', '')
            else:
                # No separators, add .00
                clean_text = clean_text + '.00'
            
            price = float(clean_text)
            logger.debug(f"Price extraction: '{price_text}' -> '{clean_text}' -> {price:.2f}")
            return price
        except ValueError as e:
            logger.error(f"Error extracting price from text: '{price_text}' -> {str(e)}")
            return 0.0
    
    def _extract_product_details(self, soup: BeautifulSoup) -> dict:
        """Extract additional product details from description and specifications."""
        details = {
            'destination_sku': '',
            'ean': '',
            'brand': '',
            'model': '',
            'color': '',
            'specifications': {},
            'categories': []
        }
        
        try:
            # Extract categories from breadcrumb navigation
            breadcrumb = soup.select('a.andes-breadcrumb__link')
            if breadcrumb:
                details['categories'] = [item.text.strip() for item in breadcrumb]
            
            # Extract from description
            description = soup.select_one('.ui-pdp-description__content')
            if description:
                desc_text = description.text.lower()
                # Look for SKU and EAN in description
                sku_match = re.search(r'sku:?\s*(\d+)', desc_text)
                if sku_match:
                    details['destination_sku'] = sku_match.group(1)
                
                ean_match = re.search(r'ean:?\s*(\d+)', desc_text)
                if ean_match:
                    details['ean'] = ean_match.group(1)
            
            # Extract from specifications table
            specs_table = soup.select('.andes-table__row')
            for row in specs_table:
                header = row.select_one('.andes-table__header')
                value = row.select_one('.andes-table__column--value')
                
                if header and value:
                    key = header.text.strip().lower()
                    val = value.text.strip()
                    
                    if 'marca' in key:
                        details['brand'] = val
                    elif 'modelo' in key:
                        details['model'] = val
                    elif 'color' in key:
                        details['color'] = val
                    else:
                        details['specifications'][header.text.strip()] = val
            
            return details
        except Exception as e:
            logger.error(f"Error extracting additional details: {str(e)}")
            return details

    def _calculate_name_similarity(self, source_name: str, target_name: str) -> float:
        """Calculate basic similarity between two product names."""
        # Normalize names
        source = source_name.lower().strip()
        target = target_name.lower().strip()
        
        # Split into words and get common words
        source_words = set(source.split())
        target_words = set(target.split())
        common_words = source_words.intersection(target_words)
        
        # Calculate similarity based on word overlap
        total_words = len(source_words.union(target_words))
        if total_words == 0:
            return 0.0
        
        return len(common_words) / total_words
    
    def _get_product_details(self, url: str) -> Optional[ScrapedProduct]:
        """Get detailed product information from a product page."""
        try:
            response = self._make_request(url)
            if not response:
                logger.error(f"No response received for URL: {url}")
                return None

            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract basic product details
            title_elem = soup.select_one('h1.ui-pdp-title')
            if not title_elem:
                logger.error(f"Could not find title element for URL: {url}")
                return None
            
            title = title_elem.text.strip()
            
            # Extract prices from the price container
            price_container = soup.select_one('.ui-pdp-price__main-container')
            if not price_container:
                logger.error(f"Could not find price container for URL: {url}")
                return None
                
            try:
                # Get original price (before discount)
                original_price_elem = price_container.select_one('.ui-pdp-price__original-value .andes-money-amount__fraction')
                original_price = 0.0
                if original_price_elem:
                    logger.debug(f"Found original price element: {original_price_elem.text}")
                    original_price = self._extract_price(original_price_elem.text)
                    logger.debug(f"Extracted original price: ${original_price}")
                
                # Get current price (with discount if applicable)
                current_price_elem = price_container.select_one('.ui-pdp-price__second-line .andes-money-amount__fraction')
                if current_price_elem:
                    logger.debug("Found discounted price element")
                else:
                    logger.debug("No discounted price found, looking for regular price")
                    current_price_elem = price_container.select_one('.andes-money-amount__fraction')
                
                if not current_price_elem:
                    logger.error(f"Could not find any price element for URL: {url}")
                    return None
                
                logger.debug(f"Current price element text: {current_price_elem.text}")
                price = self._extract_price(current_price_elem.text)
                logger.debug(f"Extracted current price: ${price}")
                
                # If we have no original price but have a current price, they're the same
                if original_price == 0.0:
                    logger.debug("No original price found, using current price")
                    original_price = price
                
                # Calculate discount percentage
                discount = 0.0
                if original_price > price:
                    discount = ((original_price - price) / original_price) * 100
                    logger.debug(f"Calculated discount: {discount:.1f}%")
                
                logger.info(f"Final prices - Original: ${original_price:.2f}, Current: ${price:.2f}, Discount: {discount:.0f}%")
                
                # Extract SKU from URL
                sku_elem = url.split('MLM')[-1].split('-')[0] if 'MLM' in url else ''
                if not sku_elem:
                    logger.warning(f"Could not extract SKU from URL: {url}")

                # Get additional product details
                details = self._extract_product_details(soup)

                # Create ScrapedProduct object
                product = ScrapedProduct(
                    source_sku='',  # Will be set later
                    marketplace='mercadolibre',
                    name=title,
                    url=url,
                    price=price,
                    original_price=original_price,
                    discount_percentage=discount,
                    destination_sku=details['destination_sku'],
                    ean=details['ean'],
                    brand=details['brand'],
                    model=details['model'],
                    color=details['color'],
                    specifications=details['specifications'],
                    categories=details['categories']
                )
                
                logger.info(f"Created ScrapedProduct object: {vars(product)}")
                return product
            except AttributeError as ae:
                logger.error(f"AttributeError while extracting data: {str(ae)}", exc_info=True)
                return None
            except Exception as e:
                logger.error(f"Unexpected error while creating ScrapedProduct: {str(e)}", exc_info=True)
                return None

        except Exception as e:
            logger.error(f"Error processing product page {url}", exc_info=True)
            return None

    def _search_products(self, query: str) -> List[ScrapedProduct]:
        """Search for products using the given query and get detailed information."""
        search_url = urljoin(self.base_url, f'/{quote(query)}#D[A:{quote(query)}]')
        logger.info(f"Searching MercadoLibre with URL: {search_url}")
        
        try:
            response = self._make_request(search_url)
            if not response:
                return []
            
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            logger.debug(f"Processing search results HTML content for URL: {search_url}")
            
            # Try different selectors for product cards to get URLs
            selectors = [
                '.ui-search-layout__item',
                '.ui-search-result__wrapper',
                '.shops__layout-item'
            ]
            
            product_cards = []
            for selector in selectors:
                product_cards = soup.select(selector)
                if product_cards:
                    logger.info(f"Found {len(product_cards)} product cards using selector: {selector}")
                    break
            
            if not product_cards:
                logger.error(f"No product cards found in search results. HTML content: {html_content[:500]}...")
                return []

            # Limit to first 10 products
            product_cards = product_cards[:10]
            logger.info(f"Processing first {len(product_cards)} product cards")
            
            products = []
            for idx, card in enumerate(product_cards):
                try:
                    # Get only the product URL from the listing
                    link_selectors = [
                        '.ui-search-link',
                        '.poly-component__title-wrapper a',
                        'a[href*="MLM"]',  # Backup selector for any link containing MLM
                    ]
                    
                    link_elem = None
                    for selector in link_selectors:
                        link_elem = card.select_one(selector)
                        if link_elem:
                            break
                    
                    if not link_elem:
                        logger.error(f"No link found in product card {idx+1}. Card HTML: {card.prettify()[:200]}...")
                        continue
                        
                    url = link_elem.get('href', '')
                    if not url:
                        logger.error(f"Empty URL in product card {idx+1}")
                        continue

                    logger.info(f"Getting details for product {idx+1} URL: {url}")
                    product = self._get_product_details(url)
                    if product:
                        products.append(product)
                        logger.info(f"Successfully processed product {idx+1}")
                    else:
                        logger.error(f"Failed to get details for product {idx+1} URL: {url}")
                        
                except Exception as e:
                    logger.error(f"Error processing product card {idx+1}", exc_info=True)
                    continue

            logger.info(f"Successfully processed {len(products)} out of {len(product_cards)} products")
            return products
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return []
    
    async def search_product(self, product: Product) -> List[ScrapedProduct]:
        """Implementation of ScraperPort.search_product method."""
        try:
            logger.info(f"Searching for product: {product.product_name} (SKU: {product.product_sku})")            
            # Run the synchronous code in a thread pool
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(None, self._search_products, product.product_name)
            
            # Set source SKU for all results
            for result in results:
                result.source_sku = product.product_sku
            
            logger.info(f"Found {len(results)} potential matches for {product.product_name}")
            return results
            
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return []
