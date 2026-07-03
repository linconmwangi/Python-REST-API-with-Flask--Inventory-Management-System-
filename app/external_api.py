"""
External API Integration - OpenFoodFacts
Handles fetching product data from the OpenFoodFacts API
"""

import requests
import logging

logger = logging.getLogger(__name__)

# OpenFoodFacts API base URL
OPENFOODFACTS_API_URL = "https://world.openfoodfacts.org/api/v0/product"

# Mock responses for testing (to avoid excessive API calls)
MOCK_PRODUCTS = {
    "5901234123457": {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "category": "Beverages",
            "ingredients_text": "Filtered water, almonds, cane sugar, calcium carbonate, sea salt, potassium citrate",
            "nutrient_levels": {
                "energy": "30 kcal",
                "fat": "2.5g",
                "carbohydrates": "1g",
                "protein": "1g"
            },
            "allergens": "Tree nuts"
        }
    },
    "5901234123458": {
        "status": 1,
        "product": {
            "product_name": "Whole Wheat Bread",
            "brands": "Nature's Harvest",
            "category": "Bakery",
            "ingredients_text": "Whole wheat flour, water, yeast, salt, sugar, vegetable oil",
            "nutrient_levels": {
                "energy": "265 kcal",
                "fat": "2.7g",
                "carbohydrates": "49g",
                "protein": "9g"
            },
            "allergens": "Gluten"
        }
    }
}


def fetch_product_by_barcode(barcode):
    """
    Fetch product data from OpenFoodFacts by barcode
    
    Args:
        barcode (str): Product barcode
        
    Returns:
        dict: Product data if found, None otherwise
    """
    try:
        # Check if in mock data first
        if barcode in MOCK_PRODUCTS:
            return MOCK_PRODUCTS[barcode]
        
        # Attempt real API call
        url = f"{OPENFOODFACTS_API_URL}/{barcode}.json"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        if data.get("status") == 1:
            return data
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching barcode {barcode}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None


def fetch_product_by_name(product_name):
    """
    Search for product data from OpenFoodFacts by name
    
    Args:
        product_name (str): Product name to search
        
    Returns:
        list: List of products found
    """
    try:
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": product_name,
            "json": 1,
            "page_size": 5
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        products = data.get("products", [])
        return products
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching for product '{product_name}': {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return []


def format_product_data(api_product):
    """
    Format API response into inventory item format
    
    Args:
        api_product (dict): Product data from API
        
    Returns:
        dict: Formatted product data
    """
    product = api_product.get("product", {})
    
    formatted_item = {
        "barcode": product.get("code", ""),
        "product_name": product.get("product_name", "Unknown Product"),
        "brands": product.get("brands", "Unknown"),
        "category": product.get("categories", "Unknown"),
        "ingredients_text": product.get("ingredients_text", ""),
        "nutrient_levels": {
            "energy": product.get("energy_value", "N/A"),
            "fat": product.get("fat_value", "N/A"),
            "carbohydrates": product.get("carbohydrates_value", "N/A"),
            "protein": product.get("proteins_value", "N/A")
        },
        "allergens": product.get("allergens", "None"),
        "price": 0.0,  # API doesn't provide price
        "quantity_in_stock": 0,  # Set by user
        "unit": "units",
        "status": "available"
    }
    
    return formatted_item


def get_product_details(identifier, search_type="barcode"):
    """
    Get product details from external API
    
    Args:
        identifier (str): Barcode or product name
        search_type (str): Either 'barcode' or 'name'
        
    Returns:
        dict or list: Product details or list of products
    """
    if search_type == "barcode":
        return fetch_product_by_barcode(identifier)
    elif search_type == "name":
        return fetch_product_by_name(identifier)
    else:
        logger.error(f"Invalid search type: {search_type}")
        return None
