import pandas as pd
from typing import List
from ...domain.ports.repository_port import ProductRepositoryPort
from ...domain.entities.product import Product, ScrapedProduct
import logging

logger = logging.getLogger(__name__)

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
        logger.info(f"Saving results to {file_path} - len: {len(results)}")
        # Filter results if needed
        if not include_no_matches:
            results = [r for r in results if r.similarity_score >= r.min_similarity_score]
            logger.info(f"Filtered {len(results)} results with similarity score >= {results[0].min_similarity_score if results else 0.2}")
        
        # Convert to DataFrame
        data = []
        for result in results:
            data.append({
                'SKU_Origen': result.source_sku,
                'Producto': result.name,
                'Precio': result.price,  # Precio con descuento si aplica
                'Precio_Lista': result.original_price,  # Precio original
                'Descuento': f"{result.discount_percentage:.0f}%" if result.discount_percentage > 0 else "",
                'URL': result.url,
                'Vendedor': result.marketplace,
                'Imagen': result.url,
                'Similitud': round(result.similarity_score, 2)
            })
        
        df = pd.DataFrame(data)
        
        # Format price columns
        df['Precio'] = df['Precio'].apply(lambda x: f"{x:,.2f}")
        df['Precio_Lista'] = df['Precio_Lista'].apply(lambda x: f"{x:,.2f}")
        
        # Save to Excel with formatting
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Resultados')
            
            # Get workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Resultados']
            
            # Add price format
            price_format = workbook.add_format({'num_format': '#,##0.00'})
            
            # Get column indices for price columns
            precio_col = df.columns.get_loc('Precio')
            precio_lista_col = df.columns.get_loc('Precio_Lista')
            
            # Apply formats
            worksheet.set_column(precio_col, precio_col, 12, price_format)
            worksheet.set_column(precio_lista_col, precio_lista_col, 12, price_format)
