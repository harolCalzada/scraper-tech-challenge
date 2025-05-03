# import logging
# import random
# import time
# import asyncio
# import requests
# import json
# import re
# import base64
# import hashlib
# import cloudscraper  # For handling Cloudflare protection
# from bs4 import BeautifulSoup
# from typing import List, Optional, Dict, Any
# from urllib.parse import urljoin, quote, urlparse, parse_qs
# from ...domain.ports.scraper_port import ScraperPort
# from ...domain.entities.product import Product, ScrapedProduct
# from ..config.settings import app_settings, default_scraper_settings
# from fake_useragent import UserAgent  # For more realistic user agents

# # Configure logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)  # Set to DEBUG to get more details

# # Add console handler if not already present
# if not logger.handlers:
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.DEBUG)
#     formatter = logging.Formatter(
#         '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n%(exc_info)s',
#         datefmt='%Y-%m-%d %H:%M:%S'
#     )
#     console_handler.setFormatter(formatter)
#     logger.addHandler(console_handler)

# def log_error(msg: str, exc_info: Exception = None) -> None:
#     """Helper function to log errors with full traceback."""
#     if exc_info:
#         logger.error(msg, exc_info=True)  # This will include the full traceback
#     else:
#         logger.error(msg)

# class WalmartScraper(ScraperPort):
#     """Implementation of scraper for Walmart Mexico using advanced anti-bot techniques."""
    
#     def __init__(self):
#         self.base_url = app_settings.supported_sites['walmart']
#         self.session = None
#         self.user_agent_generator = UserAgent()
#         self.proxy_list = None  # You would initialize this with your proxy list
#         self.current_proxy = None
#         self.cookies_obtained = False
        
#     def _get_random_proxy(self) -> Optional[Dict[str, str]]:
#         """Get a random proxy from the proxy list.
        
#         You should implement this with your proxy provider.
#         """
#         # Example implementation with a hypothetical proxy list
#         if not self.proxy_list:
#             return None
            
#         proxy = random.choice(self.proxy_list)
#         proxy_dict = {
#             "http": f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}",
#             "https": f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
#         }
#         return proxy_dict
    
#     def _init_session(self) -> None:
#         """Initialize session with advanced anti-bot techniques."""
#         try:
#             logger.info("Initializing advanced session...")
            
#             # Close existing session if any
#             self._close_session()
            
#             # Create new session with retry mechanism
#             for attempt in range(3):  # Try 3 times
#                 try:
#                     self.session = cloudscraper.create_scraper(
#                         browser={
#                             'browser': 'chrome',
#                             'platform': 'windows',
#                             'desktop': True
#                         }
#                     )
                    
#                     # Verify session was created
#                     if not self.session:
#                         raise Exception("Failed to create session")
                    
#                     # Get a realistic user agent
#                     user_agent = self.user_agent_generator.random
                    
#                     # Initialize headers first with basic configuration
#                     self.session.headers = {
#                         'User-Agent': user_agent,
#                         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#                         'Accept-Language': 'es-MX,es;q=0.8,en-US;q=0.5,en;q=0.3',
#                         'Accept-Encoding': 'gzip, deflate, br',
#                         'Connection': 'keep-alive',
#                         'Cache-Control': 'no-cache',
#                         'Pragma': 'no-cache'
#                     }
                    
#                     # Set up proxies if available
#                     self.current_proxy = self._get_random_proxy()
#                     if self.current_proxy:
#                         self.session.proxies.update(self.current_proxy)
#                         logger.info(f"Using proxy: {self.current_proxy}")
                    
#                     # Verify headers were set
#                     if not hasattr(self.session, 'headers'):
#                         raise Exception("Failed to set session headers")
                    
#                     # Set advanced headers
#                     self._set_advanced_headers(user_agent)
                    
#                     # Initialize browser fingerprint
#                     self._generate_browser_fingerprint()
#                     logger.info("Advanced session initialized with browser fingerprinting")
                    
#                     # Test the session with a simple request
#                     test_response = self.session.get(
#                         self.base_url,
#                         timeout=10,
#                         allow_redirects=True
#                     )
#                     test_response.raise_for_status()
                    
#                     # If we got here, session is working
#                     logger.info("Session successfully tested")
                    
#                     # Preload cookies and tokens
#                     self._warm_up_session()
#                     break  # Success, exit retry loop
                    
#                 except Exception as e:
#                     log_error(f"Session initialization attempt {attempt + 1} failed", e)
#                     if attempt == 2:  # Last attempt
#                         raise  # Re-raise the last error
#                     time.sleep(random.uniform(1, 3))  # Wait before retry
                
#         except Exception as e:
#             log_error(f"Error initializing session: {str(e)}", e)
#             self.session = None  # Reset session on error
#             raise
            
#     def _set_advanced_headers(self, user_agent: str) -> None:
#         """Set advanced headers that closely mimic a real browser."""
#         # Standard headers with advanced properties
#         self.session.headers.update({
#             'User-Agent': user_agent,
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#             'Accept-Language': 'es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Connection': 'keep-alive',
#             'Upgrade-Insecure-Requests': '1',
#             'Sec-Fetch-Dest': 'document',
#             'Sec-Fetch-Mode': 'navigate',
#             'Sec-Fetch-Site': 'none',
#             'Sec-Fetch-User': '?1',
#             'sec-ch-ua': '"Google Chrome";v="135", "Chromium";v="135", "Not-A.Brand";v="99"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'DNT': '1',
#             'Cache-Control': 'max-age=0',
#             'TE': 'trailers',
#             'Referer': 'https://www.google.com.mx/',
#             'Priority': 'u=0, i',
#         })
        
#     def _generate_browser_fingerprint(self) -> Dict[str, Any]:
#         """Generate a realistic browser fingerprint."""
#         # This would be a more complex implementation in a real scraper
#         # Here's a simplified version
#         return {
#             'screen': {
#                 'width': random.choice([1920, 1366, 1440, 2560]),
#                 'height': random.choice([1080, 768, 900, 1440])
#             },
#             'navigator': {
#                 'userAgent': self.session.headers['User-Agent'],
#                 'language': 'es-PE',
#                 'platform': random.choice(['Win32', 'MacIntel']),
#                 'hardwareConcurrency': random.choice([4, 8, 12, 16]),
#                 'deviceMemory': random.choice([8, 16, 32])
#             },
#             'canvas': hashlib.md5(str(time.time()).encode()).hexdigest(),
#             'webgl': hashlib.sha256(str(time.time()).encode()).hexdigest(),
#             'fonts': ['Arial', 'Courier', 'Times New Roman']
#         }
            
#     def _warm_up_session(self) -> None:
#         """Warm up the session by visiting multiple pages in a natural pattern."""
#         if not self.session:
#             logger.error("Cannot warm up session: Session not initialized")
#             return
            
#         try:
#             # Visit the homepage first
#             logger.info("Warming up session by visiting homepage...")
            
#             # Ensure we have basic headers set
#             if not hasattr(self.session, 'headers'):
#                 self.session.headers = {}
            
#             response = self.session.get(
#                 self.base_url,
#                 timeout=30,
#                 allow_redirects=True
#             )
            
#             if not response.ok:
#                 logger.warning(f"Homepage visit failed with status {response.status_code}")
#                 return
                
#             # Extract cookies and tokens if needed
#             self._extract_tokens(response.text)
            
#             # Simulate a real user by visiting a few category pages
#             categories = [
#                 '/departamentos/',
#                 '/super/',
#                 '/productos/electronicos/',
#                 '/productos/hogar/'
#             ]
            
#             # Visit 1-2 random categories with delays
#             for _ in range(random.randint(1, 2)):
#                 category = random.choice(categories)
#                 category_url = urljoin(self.base_url, category)
                
#                 # Add natural delay between page visits
#                 time.sleep(random.uniform(3, 7))
                
#                 logger.info(f"Visiting category page: {category}")
#                 try:
#                     cat_response = self.session.get(
#                         category_url,
#                         timeout=30,
#                         allow_redirects=True
#                     )
                    
#                     # More natural behavior - scroll simulation through headers
#                     if hasattr(self.session, 'headers'):
#                         self.session.headers.update({'Referer': category_url})
#                 except Exception as e:
#                     logger.warning(f"Failed to visit category {category}: {str(e)}")
#                     continue
            
#             # Mark that we've successfully obtained cookies
#             self.cookies_obtained = True
#             logger.info("Session warmed up with multiple page visits")
            
#         except Exception as e:
#             log_error(f"Error during session warm-up: {str(e)}", e)
#             self.cookies_obtained = False
    
#     def _extract_tokens(self, html_content: str) -> None:
#         """Extract any security tokens from the page."""
#         # Look for common token patterns in the HTML
#         # This would need to be customized based on Walmart's specific implementation
#         token_patterns = [
#             r'csrf_token\s*=\s*["\']([^"\']+)["\']',
#             r'token["\']:\s*["\']([^"\']+)["\']',
#             r'security_token["\']:\s*["\']([^"\']+)["\']'
#         ]
        
#         for pattern in token_patterns:
#             match = re.search(pattern, html_content)
#             if match:
#                 token = match.group(1)
#                 logger.info(f"Found security token: {token[:10]}...")
#                 # Add the token to headers or cookies as needed
#                 self.session.headers.update({'X-CSRF-Token': token})
#                 return
    
#     def _close_session(self) -> None:
#         """Close the session."""
#         if self.session:
#             self.session.close()
#             self.session = None
#             self.cookies_obtained = False
    
#     def _make_request(self, url: str, retries: int = None) -> Optional[str]:
#         """Make HTTP request with advanced anti-bot techniques."""
#         if retries is None:
#             retries = default_scraper_settings.max_retries
        
#         for attempt in range(retries):
#             try:
#                 # Add realistic delay between requests
#                 delay = random.uniform(
#                     default_scraper_settings.request_delay * 1.5,  # Increase default delay
#                     default_scraper_settings.request_delay * 3
#                 ) * (1.5 ** attempt)  # Less aggressive backoff
#                 time.sleep(delay)
                
#                 # Initialize or refresh session if needed
#                 if not self.session or attempt > 0:
#                     self._init_session()
                
#                 # Update fingerprint and headers for each request
#                 self._rotate_fingerprint()
                
#                 # Add URL-specific referrer for more natural browsing pattern
#                 parsed_url = urlparse(url)
#                 path_parts = parsed_url.path.strip('/').split('/')
                
#                 if len(path_parts) > 1:
#                     # If it's a deep path, use parent path as referrer
#                     parent_path = '/'.join(path_parts[:-1])
#                     parent_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{parent_path}/"
#                     self.session.headers.update({'Referer': parent_url})
                
#                 # Make the request with proper timing
#                 logger.info(f"Making request to {url}")
                
#                 # Pre-request delay simulation (thinking time)
#                 time.sleep(random.uniform(0.5, 2))
                
#                 # Actual request with appropriate timeout
#                 response = self.session.get(
#                     url,
#                     timeout=30,
#                     allow_redirects=True
#                 )
                
#                 # Check if the request was successful
#                 response.raise_for_status()
                
#                 # Check for verification page
#                 if self._is_verification_page(response.text):
#                     logger.warning("Bot detection triggered, rotating proxy and session...")
#                     # Rotate proxy and session completely
#                     self._close_session()
#                     time.sleep(random.uniform(10, 15))
#                     continue
                
#                 # Successful response - simulate reading time
#                 content_length = len(response.text)
#                 # Human reading simulation - longer delay for more content
#                 reading_time = min(random.uniform(2, 5), content_length / 50000)
#                 time.sleep(reading_time)
                
#                 # API authentication check
#                 if "API key" in response.text or "authentication failed" in response.text.lower():
#                     logger.warning("API authentication issue detected")
#                     self._rotate_fingerprint()
#                     continue
                    
#                 return response.text
                
#             except Exception as e:
#                 log_error(f"Request error on attempt {attempt + 1}: {str(e)}", e, exc_info=True)
#                 # More aggressive session reset
#                 self._close_session()
#                 # Longer delay after error
#                 time.sleep(random.uniform(5, 10))
            
#             if attempt < retries - 1:
#                 delay = random.uniform(3 ** attempt, 3 ** (attempt + 1))
#                 logger.info(f"Waiting {delay:.2f}s before retry {attempt + 2}...")
#                 time.sleep(delay)
#             else:
#                 logger.error(f"Failed to fetch {url} after {retries} attempts")
#                 return None
    
#     def _rotate_fingerprint(self) -> None:
#         """Rotate browser fingerprint and related headers."""
#         # Change user agent but not too frequently (seems more natural)
#         if random.random() < 0.2:  # 20% chance to change
#             new_user_agent = self.user_agent_generator.random
#             self.session.headers.update({'User-Agent': new_user_agent})
        
#         # Rotate other fingerprinting headers
#         self.session.headers.update({
#             # Randomize client hints
#             'sec-ch-ua-platform': random.choice(['"Windows"', '"macOS"']),
#             'sec-ch-ua': random.choice([
#                 '"Google Chrome";v="135", "Chromium";v="135", "Not-A.Brand";v="99"',
#                 '"Google Chrome";v="133", "Chromium";v="133", "Not-A.Brand";v="99"',
#                 '"Google Chrome";v="131", "Chromium";v="131", "Not-A.Brand";v="99"'
#             ]),
            
#             # Randomize viewport and device memory
#             'Viewport-Width': str(random.choice([1366, 1440, 1920, 2560])),
#             'Device-Memory': str(random.choice([4, 8, 16]))
#         })
        
#         # Possibly rotate proxy if available
#         if self.proxy_list and random.random() < 0.3:  # 30% chance to rotate proxy
#             self.current_proxy = self._get_random_proxy()
#             if self.current_proxy:
#                 self.session.proxies.update(self.current_proxy)
#                 logger.info(f"Rotated proxy to: {self.current_proxy}")
    
#     def _is_verification_page(self, html_content: str) -> bool:
#         """Enhanced detection of verification/CAPTCHA pages."""
#         verification_indicators = [
#             "Verifica tu identidad",
#             "verify your identity",
#             "captcha",
#             "security check",
#             "suspicious activity",
#             "robot",
#             "automated",
#             "demasiadas solicitudes",
#             "too many requests",
#             "acceso bloqueado",
#             "access denied",
#             "challenge",
#             "unusual activity"
#         ]
#         html_content_lower = html_content.lower()
        
#         # Look for verification indicators
#         if any(indicator.lower() in html_content_lower for indicator in verification_indicators):
#             return True
            
#         # Check for redirects to verification pages
#         redirect_patterns = [
#             r'window\.location\s*=\s*["\']([^"\']*verify[^"\']*)["\']',
#             r'window\.location\.href\s*=\s*["\']([^"\']*security[^"\']*)["\']',
#             r'window\.location\.replace\(["\']([^"\']*captcha[^"\']*)["\']'
#         ]
        
#         for pattern in redirect_patterns:
#             if re.search(pattern, html_content):
#                 return True
        
#         # Check for very short responses (often indicates blocking)
#         if len(html_content) < 1000:
#             soup = BeautifulSoup(html_content, 'html.parser')
#             # If short content and no significant content, likely blocked
#             if len(soup.find_all(['p', 'div', 'span', 'a'])) < 5:
#                 return True
                
#         return False
    
#     def _extract_price(self, price_text: str) -> float:
#         """Extract price from text."""
#         try:
#             # Remove currency symbol and commas, then convert to float
#             cleaned_price = price_text.replace('$', '').replace(',', '').strip()
#             return float(cleaned_price)
#         except (ValueError, AttributeError) as e:
#             logger.error(f"Error extracting price from {price_text}: {str(e)}")
#             return 0.0
    
#     def _search_products(self, query: str) -> List[ScrapedProduct]:
#         """Internal method to search for products using the given query."""
#         # Initialize session if not already initialized
#         if not self.session:
#             try:
#                 self._init_session()
#             except Exception as e:
#                 log_error("Failed to initialize session", e)
#                 return []
        
#         if not self.session:
#             log_error("Session initialization failed")
#             return []
            
#         search_url = urljoin(self.base_url, f'/search/?q={quote(query)}')
#         logger.info(f"Searching Walmart with URL: {search_url}")
        
#         try:
#             # Ensure we have basic headers
#             if not hasattr(self.session, 'headers'):
#                 self.session.headers = {
#                     'User-Agent': self.user_agent_generator.random,
#                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#                     'Accept-Language': 'es-MX,es;q=0.8,en-US;q=0.5,en;q=0.3',
#                     'Connection': 'keep-alive'
#                 }
            
#             # Make the request
#             try:
#                 html_content = self._make_request(search_url)
#             except Exception as e:
#                 log_error("Failed to fetch HTML content", e)
#                 return []
                
#             if not html_content:
#                 logger.warning("No HTML content received from Walmart")
#                 return []
            
#             logger.info("Parsing product cards from HTML...")
#             soup = BeautifulSoup(html_content, 'html.parser')
            
#             # Sometimes products are in a JSON script tag for client-side rendering
#             # Try to extract that first
#             script_data = self._extract_json_from_script_tags(soup)
#             if script_data:
#                 return self._parse_script_data(script_data, query)
            
#             # Otherwise fallback to traditional HTML parsing
#             # Find all product cards
#             product_cards = soup.find_all('div', class_='flex flex-column w-100')
#             logger.info(f"Found {len(product_cards)} product cards on page")
            
#             # If no cards found with primary selector, try alternative selectors
#             if not product_cards:
#                 product_cards = soup.select('[data-automation-id="product"]')
                
#             if not product_cards:
#                 product_cards = soup.select('.product-card')
                
#             results = []
#             for card in product_cards:
#                 try:
#                     # Extract product information using more general selectors
#                     title_elem = card.find('span', {'data-automation-id': 'product-title'}) or \
#                                 card.find('span', class_='w_iUH7') or \
#                                 card.select_one('[class*="title"]')
                    
#                     price_elem = card.find('span', {'data-automation-id': 'product-price'}) or \
#                                card.find('div', class_='b_wE0H') or \
#                                card.select_one('[class*="price"]')
                               
#                     link_elem = card.find('a', {'data-automation-id': 'product-link'}) or \
#                               card.find('a', class_='absolute w-100 h-100 z-1') or \
#                               card.select_one('a')
                    
#                     if not all([title_elem, price_elem, link_elem]):
#                         continue
                    
#                     title = title_elem.text.strip()
#                     price = self._extract_price(price_elem.text.strip())
#                     url = urljoin(self.base_url, link_elem.get('href', ''))
                    
#                     # Skip if missing essential data
#                     if not title or not price or not url:
#                         continue
                    
#                     results.append(
#                         ScrapedProduct(
#                             id=str(int(time.time() * 1000)),
#                             name=title,
#                             price=price,
#                             url=url,
#                             source='walmart',
#                             source_sku='',
#                             marketplace='walmart',
#                             similarity_score=0.0
#                         )
#                     )
                    
#                 except Exception as e:
#                     logger.error(f"Error extracting product data: {str(e)}")
#                     continue
            
#             return results
            
#         except Exception as e:
#             log_error(f"Error searching products: {str(e)}", e)
#             return []
            
#         finally:
#             # Don't close the session every time - keep it warm
#             # Only close if error detected
#             if self._is_session_compromised():
#                 self._close_session()
                
#     def _is_session_compromised(self) -> bool:
#         """Check if the current session seems to be compromised or blocked."""
#         # This is a simplified check - you would implement more robust detection
#         if not self.session:
#             return True
            
#         if not self.cookies_obtained:
#             return True
            
#         # Check if essential cookies are missing
#         essential_cookies = ['session-id', 'JSESSIONID', 'auth']  # Example names
#         cookies_present = any(cookie in self.session.cookies for cookie in essential_cookies)
#         return not cookies_present
                
#     def _extract_json_from_script_tags(self, soup: BeautifulSoup) -> Optional[Dict]:
#         """Extract product data from JSON in script tags."""
#         # Look for script tags containing product data
#         for script in soup.find_all('script', {'type': 'application/json'}):
#             try:
#                 data = json.loads(script.string)
#                 # Check if this contains product data
#                 if 'products' in data or 'items' in data or 'results' in data:
#                     return data
#             except (json.JSONDecodeError, TypeError):
#                 continue
                
#         # Try looking in other script tags
#         for script in soup.find_all('script'):
#             try:
#                 script_text = script.string or ""
#                 if 'window.__INITIAL_STATE__' in script_text:
#                     # Extract the JSON part
#                     json_str = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', script_text, re.DOTALL)
#                     if json_str:
#                         return json.loads(json_str.group(1))
#             except (json.JSONDecodeError, TypeError, AttributeError):
#                 continue
                
#         return None
        
#     def _parse_script_data(self, data: Dict, query: str) -> List[ScrapedProduct]:
#         """Parse product data from extracted script JSON."""
#         results = []
        
#         # Different possible structures in the JSON
#         products = data.get('products', []) or data.get('items', []) or data.get('results', [])
        
#         if isinstance(products, dict):
#             # Sometimes it's a dict with nested arrays
#             for key, items in products.items():
#                 if isinstance(items, list):
#                     products = items
#                     break
        
#         for product in products:
#             try:
#                 # Extract data from the JSON structure
#                 product_id = product.get('id', '') or product.get('productId', '')
#                 name = product.get('name', '') or product.get('title', '')
                
#                 # Price can be nested in different ways
#                 price = 0.0
#                 price_info = product.get('price', {}) or product.get('priceInfo', {})
#                 if isinstance(price_info, dict):
#                     price = float(price_info.get('currentPrice', 0) or 
#                                price_info.get('price', 0) or 
#                                price_info.get('amount', 0))
#                 elif isinstance(price_info, (int, float, str)):
#                     try:
#                         price = float(price_info)
#                     except (ValueError, TypeError):
#                         price = 0.0
                
#                 # URL construction
#                 url_path = product.get('url', '') or product.get('productUrl', '')
#                 url = urljoin(self.base_url, url_path) if url_path else ''
                
#                 if not all([name, price > 0, url]):
#                     continue
                    
#                 results.append(
#                     ScrapedProduct(
#                         id=str(product_id) or str(int(time.time() * 1000)),
#                         name=name,
#                         price=price,
#                         url=url,
#                         source='walmart',
#                         source_sku='',
#                         marketplace='walmart',
#                         similarity_score=0.0
#                     )
#                 )
                
#             except Exception as e:
#                 logger.error(f"Error parsing product from script data: {str(e)}")
#                 continue
                
#         return results
        

    
#     async def search_product(self, product: Product) -> List[ScrapedProduct]:
#         """Implementation of ScraperPort.search_product method.
        
#         Args:
#             product: Product entity containing search criteria
            
#         Returns:
#             List of ScrapedProduct entities found matching the criteria
#         """
#         logger.info(f"Searching for product: {product.product_name} (SKU: {product.product_sku})")
        
#         # Run the synchronous requests code in a thread pool
#         loop = asyncio.get_event_loop()
#         results = await loop.run_in_executor(None, self._search_products, product.product_name)
        
#         # Set source SKU for all results
#         for result in results:
#             result.source_sku = product.product_sku
        
#         logger.info(f"Found {len(results)} potential matches for {product.product_name}")
#         return results