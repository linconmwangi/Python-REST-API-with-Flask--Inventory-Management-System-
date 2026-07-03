"""
Mock Database for Inventory Management System
Simulates a database with OpenFoodFacts API-like schema
"""

# Mock inventory database - array to simulate data storage
inventory_db = [
    {
        "id": 1,
        "barcode": "5901234123457",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "category": "Beverages",
        "ingredients_text": "Filtered water, almonds, cane sugar, calcium carbonate, sea salt, potassium citrate",
        "price": 3.99,
        "quantity_in_stock": 150,
        "unit": "liters",
        "nutrient_levels": {
            "energy": "30 kcal",
            "fat": "2.5g",
            "carbohydrates": "1g",
            "protein": "1g"
        },
        "allergens": "Tree nuts",
        "status": "available"
    },
    {
        "id": 2,
        "barcode": "5901234123458",
        "product_name": "Whole Wheat Bread",
        "brands": "Nature's Harvest",
        "category": "Bakery",
        "ingredients_text": "Whole wheat flour, water, yeast, salt, sugar, vegetable oil",
        "price": 2.49,
        "quantity_in_stock": 50,
        "unit": "loaves",
        "nutrient_levels": {
            "energy": "265 kcal",
            "fat": "2.7g",
            "carbohydrates": "49g",
            "protein": "9g"
        },
        "allergens": "Gluten",
        "status": "available"
    },
    {
        "id": 3,
        "barcode": "5901234123459",
        "product_name": "Extra Virgin Olive Oil",
        "brands": "Colavita",
        "category": "Oils",
        "ingredients_text": "100% Extra Virgin Olive Oil",
        "price": 12.99,
        "quantity_in_stock": 30,
        "unit": "bottles",
        "nutrient_levels": {
            "energy": "884 kcal",
            "fat": "100g",
            "carbohydrates": "0g",
            "protein": "0g"
        },
        "allergens": "None",
        "status": "available"
    }
]


def get_next_id():
    """Get the next available ID"""
    if not inventory_db:
        return 1
    return max(item["id"] for item in inventory_db) + 1


def get_all_items():
    """Retrieve all inventory items"""
    return inventory_db


def get_item_by_id(item_id):
    """Retrieve a single item by ID"""
    for item in inventory_db:
        if item["id"] == item_id:
            return item
    return None


def add_item(item):
    """Add a new item to inventory"""
    item["id"] = get_next_id()
    inventory_db.append(item)
    return item


def update_item(item_id, updated_data):
    """Update an existing item"""
    for item in inventory_db:
        if item["id"] == item_id:
            item.update(updated_data)
            return item
    return None


def delete_item(item_id):
    """Delete an item from inventory"""
    global inventory_db
    initial_length = len(inventory_db)
    inventory_db = [item for item in inventory_db if item["id"] != item_id]
    return initial_length != len(inventory_db)


def search_items(query, search_field="product_name"):
    """Search items by a field"""
    results = []
    query_lower = query.lower()
    for item in inventory_db:
        if search_field in item and query_lower in str(item[search_field]).lower():
            results.append(item)
    return results


def reset_database():
    """Reset database to initial state (useful for testing)"""
    global inventory_db
    inventory_db = [
        {
            "id": 1,
            "barcode": "5901234123457",
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "category": "Beverages",
            "ingredients_text": "Filtered water, almonds, cane sugar, calcium carbonate, sea salt, potassium citrate",
            "price": 3.99,
            "quantity_in_stock": 150,
            "unit": "liters",
            "nutrient_levels": {
                "energy": "30 kcal",
                "fat": "2.5g",
                "carbohydrates": "1g",
                "protein": "1g"
            },
            "allergens": "Tree nuts",
            "status": "available"
        },
        {
            "id": 2,
            "barcode": "5901234123458",
            "product_name": "Whole Wheat Bread",
            "brands": "Nature's Harvest",
            "category": "Bakery",
            "ingredients_text": "Whole wheat flour, water, yeast, salt, sugar, vegetable oil",
            "price": 2.49,
            "quantity_in_stock": 50,
            "unit": "loaves",
            "nutrient_levels": {
                "energy": "265 kcal",
                "fat": "2.7g",
                "carbohydrates": "49g",
                "protein": "9g"
            },
            "allergens": "Gluten",
            "status": "available"
        },
        {
            "id": 3,
            "barcode": "5901234123459",
            "product_name": "Extra Virgin Olive Oil",
            "brands": "Colavita",
            "category": "Oils",
            "ingredients_text": "100% Extra Virgin Olive Oil",
            "price": 12.99,
            "quantity_in_stock": 30,
            "unit": "bottles",
            "nutrient_levels": {
                "energy": "884 kcal",
                "fat": "100g",
                "carbohydrates": "0g",
                "protein": "0g"
            },
            "allergens": "None",
            "status": "available"
        }
    ]
