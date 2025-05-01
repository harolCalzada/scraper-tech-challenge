import pandas as pd
from typing import List
from ...domain.ports.repository_port import ProductRepositoryPort
from ...domain.entities.product import Product, ScrapedProduct

class ExcelRepository(ProductRepositoryPort):
    """Implementation of repository for Excel file handling."""
    
    def load_products(self, file_path: str) -> List[Product]:
        """Load products from Excel file."""
        df = pd.read_excel(file_path)
        
        # Convert DataFrame rows to Product entities
        products = []
        for _, row in df.iterrows():
            product = Product(
                product_sku=str(row['SkuProducto']),
                product_name=str(row['Producto']),
                product_line=str(row['Linea']),
                product_group=str(row['Grupo']),
                category=str(row['Categoria']),
                subcategory=str(row['SubCategoria']),
                sub_subcategory=str(row['SubSubCatego']),
                area=str(row['Area']),
                status=str(row['Estado'])
            )
            products.append(product)
        
        return products
    
    def save_results(self, file_path: str, results: List[ScrapedProduct], include_no_matches: bool = False) -> None:
        """Save scraped products to Excel file."""
        # Filter results if needed
        if not include_no_matches:
            results = [r for r in results if r.found_match]
        
        # Convert to DataFrame
        data = []
        for result in results:
            data.append({
                'SKU_Origen': result.source_sku,
                'Producto': result.name,
                'Precio': result.price,
                'Precio_Lista': result.price,
                'URL': result.url,
                'Vendedor': result.marketplace,
                'Imagen': result.url,
                'Similitud': round(result.similarity_score, 2)
            })
        
        df = pd.DataFrame(data)
        
        # Save to Excel
        df.to_excel(file_path, index=False)
