from abc import ABC, abstractmethod
from typing import List
from ..entities.product import Product, ScrapedProduct

class ProductRepositoryPort(ABC):
    """Port defining the contract for product data persistence."""
    
    @abstractmethod
    def load_products(self, file_path: str) -> List[Product]:
        """
        Load products from the input Excel file.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            List of Product entities
        """
        pass
    
    @abstractmethod
    def save_results(self, file_path: str, results: List[ScrapedProduct], include_no_matches: bool = False) -> None:
        """
        Save scraped products to output file.
        
        Args:
            file_path: Path where to save the results
            results: List of ScrapedProduct entities to save
            include_no_matches: If True, include products with similarity score below threshold
        
        The output CSV will contain the following columns:
        - SKU_Origen: Original SKU from input Excel
        - Producto: Found product title
        - Precio: Current price
        - Precio_Lista: List price (if available)
        - URL: Product URL
        - Vendedor: Marketplace name (walmart/mercadolibre) + specific seller if available
        - Imagen: Product image URL
        - Similitud: Similarity score with original product
        """
        pass
