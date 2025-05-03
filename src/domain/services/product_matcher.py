from typing import Optional
from difflib import SequenceMatcher
import logging
from ..entities.product import Product, ScrapedProduct

logger = logging.getLogger(__name__)

class ProductMatcher:
    """Service for matching products based on similarity criteria."""
    
    def __init__(self, min_similarity_score: float = 0.6):
        self.min_similarity_score = min_similarity_score
        self.weights = {
            'sku': 0.3,      # 30% weight if SKUs match
            'name': 0.3,     # 30% weight for name similarity
            'category': 0.2,  # 20% weight for category matches
            'brand': 0.1,    # 10% weight if brands match
            'model': 0.1     # 10% weight if models match
        }
    
    def _calculate_sku_similarity(self, source: Product, target: ScrapedProduct) -> float:
        """Calculate similarity score based on SKU match."""
        if source.product_sku and target.destination_sku:
            if source.product_sku.lower().strip() == target.destination_sku.lower().strip():
                logger.debug(f"SKU match found: {source.product_sku}")
                return self.weights['sku']
        return 0.0
    
    def _calculate_name_similarity(self, source: Product, target: ScrapedProduct) -> float:
        """Calculate similarity score based on product name."""
        # Clean and normalize names
        source_name = source.product_name.lower().strip()
        target_name = target.name.lower().strip()
        
        # Split names into words
        source_words = set(source_name.split())
        target_words = set(target_name.split())
        
        # Calculate word overlap
        common_words = source_words.intersection(target_words)
        total_words = source_words.union(target_words)
        word_overlap_score = len(common_words) / len(total_words) if total_words else 0
        
        # Calculate sequence similarity
        sequence_similarity = SequenceMatcher(None, source_name, target_name).ratio()
        
        # Combine both scores (60% sequence similarity, 40% word overlap)
        combined_score = (sequence_similarity * 0.6) + (word_overlap_score * 0.4)
        final_score = combined_score * self.weights['name']
        
        logger.debug(f"Name similarity for '{source_name}' vs '{target_name}':")
        logger.debug(f"  Sequence similarity: {sequence_similarity:.2f}")
        logger.debug(f"  Word overlap: {word_overlap_score:.2f}")
        logger.debug(f"  Combined score: {combined_score:.2f}")
        logger.debug(f"  Final weighted score: {final_score:.2f}")
        
        return final_score
    
    def _calculate_category_similarity(self, source: Product, target: ScrapedProduct) -> float:
        """Calculate similarity score based on category matches."""
        if not hasattr(target, 'categories') or not target.categories:
            logger.debug("No target categories available")
            return 0.0
            
        # Prepare source categories
        source_categories = [source.category, source.subcategory, source.sub_subcategory]
        source_categories = [cat.lower().strip() for cat in source_categories if cat and cat.strip()]
        
        # Prepare target categories
        target_categories = [cat.lower().strip() for cat in target.categories if cat and cat.strip()]
        
        logger.debug(f"Source categories: {source_categories}")
        logger.debug(f"Target categories: {target_categories}")
        
        if not source_categories or not target_categories:
            logger.debug("Either source or target categories are empty after cleaning")
            return 0.0
        
        # Calculate word-based similarity for each category pair
        max_similarities = []
        for source_cat in source_categories:
            source_words = set(source_cat.split())
            cat_similarities = []
            
            for target_cat in target_categories:
                target_words = set(target_cat.split())
                
                # Check for exact match first
                if source_cat == target_cat:
                    cat_similarities.append(1.0)
                    logger.debug(f"Exact match found: '{source_cat}' = '{target_cat}'")
                    continue
                
                # Calculate word overlap for partial matches
                common_words = source_words.intersection(target_words)
                total_words = len(source_words.union(target_words))
                
                if total_words > 0:
                    # Base similarity on word overlap
                    similarity = len(common_words) / total_words
                    
                    # Boost score if one string contains the other
                    if source_cat in target_cat or target_cat in source_cat:
                        similarity = min(1.0, similarity * 1.5)  # 50% boost but cap at 1.0
                    
                    cat_similarities.append(similarity)
                    logger.debug(f"Comparing '{source_cat}' with '{target_cat}': {similarity:.2f}")
                    logger.debug(f"  Common words: {common_words}")
            
            if cat_similarities:
                max_similarities.append(max(cat_similarities))
        
        if max_similarities:
            # Average of best matches for each source category
            category_score = sum(max_similarities) / len(source_categories)
            score = category_score * self.weights['category']
            logger.debug(f"Category similarities: {max_similarities}")
            logger.debug(f"Final category score: {category_score:.2f} (weighted: {score:.2f})")
            return score
            
        logger.debug("No category matches found")
        return 0.0
    
    def _calculate_brand_similarity(self, source: Product, target: ScrapedProduct) -> float:
        """Calculate similarity score based on brand match."""
        if hasattr(source, 'brand') and target.brand:
            if source.brand.lower() == target.brand.lower():
                logger.debug(f"Brand match found: {source.brand}")
                return self.weights['brand']
        return 0.0
    
    def _calculate_model_similarity(self, source: Product, target: ScrapedProduct) -> float:
        """Calculate similarity score based on model match."""
        if hasattr(source, 'model') and target.model:
            if source.model.lower() == target.model.lower():
                logger.debug(f"Model match found: {source.model}")
                return self.weights['model']
        return 0.0
    
    def calculate_similarity(self, source: Product, target: ScrapedProduct) -> float:
        """
        Calculate overall similarity score between source and target products.
        Returns a score between 0 and 1.
        """
        try:
            # Calculate individual similarity scores
            sku_score = self._calculate_sku_similarity(source, target)
            name_score = self._calculate_name_similarity(source, target)
            category_score = self._calculate_category_similarity(source, target)
            brand_score = self._calculate_brand_similarity(source, target)
            model_score = self._calculate_model_similarity(source, target)
            
            # Calculate total score
            total_score = sum([sku_score, name_score, category_score, brand_score, model_score])
            
            logger.info(f"Similarity scores for {target.name}:")
            logger.info(f"  SKU: {sku_score:.2f}")
            logger.info(f"  Name: {name_score:.2f}")
            logger.info(f"  Category: {category_score:.2f}")
            logger.info(f"  Brand: {brand_score:.2f}")
            logger.info(f"  Model: {model_score:.2f}")
            logger.info(f"  Total: {total_score:.2f}")
            
            return total_score
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}", exc_info=True)
            return 0.0
    
    def is_match(self, source: Product, target: ScrapedProduct) -> bool:
        """
        Determine if two products match based on similarity score.
        Uses the min_similarity_score from the target ScrapedProduct.
        """
        score = self.calculate_similarity(source, target)
        target.similarity_score = score
        logger.debug(f"Checking match for {target.name} - Score: {score:.2f}, Min required: {target.min_similarity_score}")
        return score >= target.min_similarity_score  # Use ScrapedProduct's min_similarity_score
