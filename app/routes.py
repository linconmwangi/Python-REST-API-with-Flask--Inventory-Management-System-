"""
Flask Routes for Inventory Management System
Implements RESTful API endpoints for CRUD operations
"""

from flask import Blueprint, request, jsonify
from app import database
from app import external_api
import logging

logger = logging.getLogger(__name__)

# Create blueprint for API routes
api = Blueprint("api", __name__, url_prefix="/inventory")


# ==================== READ OPERATIONS ====================

@api.route("", methods=["GET"])
def get_all_items():
    """
    GET /inventory
    Fetch all inventory items
    
    Returns:
        JSON: List of all items with metadata
    """
    try:
        items = database.get_all_items()
        return jsonify({
            "status": "success",
            "message": "All inventory items retrieved",
            "count": len(items),
            "data": items
        }), 200
    except Exception as e:
        logger.error(f"Error fetching all items: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve items"
        }), 500


@api.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """
    GET /inventory/<id>
    Fetch a single inventory item by ID
    
    Args:
        item_id (int): The ID of the item to retrieve
        
    Returns:
        JSON: Item details or error message
    """
    try:
        item = database.get_item_by_id(item_id)
        if item:
            return jsonify({
                "status": "success",
                "message": "Item retrieved",
                "data": item
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Item with ID {item_id} not found"
            }), 404
    except Exception as e:
        logger.error(f"Error fetching item {item_id}: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve item"
        }), 500


@api.route("/search", methods=["GET"])
def search_items():
    """
    GET /inventory/search?q=<query>&field=<field>
    Search inventory items
    
    Query Parameters:
        q (str): Search query
        field (str): Field to search in (default: product_name)
        
    Returns:
        JSON: List of matching items
    """
    try:
        query = request.args.get("q", "")
        search_field = request.args.get("field", "product_name")
        
        if not query:
            return jsonify({
                "status": "error",
                "message": "Search query is required"
            }), 400
        
        results = database.search_items(query, search_field)
        return jsonify({
            "status": "success",
            "message": "Search completed",
            "count": len(results),
            "data": results
        }), 200
    except Exception as e:
        logger.error(f"Error searching items: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Search failed"
        }), 500


# ==================== CREATE OPERATIONS ====================

@api.route("", methods=["POST"])
def create_item():
    """
    POST /inventory
    Add a new inventory item
    
    JSON Body:
        {
            "barcode": string,
            "product_name": string,
            "brands": string,
            "category": string,
            "price": float,
            "quantity_in_stock": int,
            "unit": string,
            "status": string
        }
        
    Returns:
        JSON: Created item with ID
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["product_name", "price", "quantity_in_stock"]
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required field: {field}"
                }), 400
        
        # Set defaults for optional fields
        item = {
            "barcode": data.get("barcode", ""),
            "product_name": data.get("product_name"),
            "brands": data.get("brands", "Unknown"),
            "category": data.get("category", "General"),
            "ingredients_text": data.get("ingredients_text", ""),
            "price": float(data.get("price")),
            "quantity_in_stock": int(data.get("quantity_in_stock")),
            "unit": data.get("unit", "units"),
            "nutrient_levels": data.get("nutrient_levels", {}),
            "allergens": data.get("allergens", "None"),
            "status": data.get("status", "available")
        }
        
        created_item = database.add_item(item)
        return jsonify({
            "status": "success",
            "message": "Item created successfully",
            "data": created_item
        }), 201
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": f"Invalid data format: {str(e)}"
        }), 400
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to create item"
        }), 500


@api.route("/from-api", methods=["POST"])
def create_item_from_api():
    """
    POST /inventory/from-api
    Create inventory item by fetching from external API
    
    JSON Body:
        {
            "identifier": string,
            "search_type": "barcode" | "name",
            "price": float,
            "quantity_in_stock": int
        }
        
    Returns:
        JSON: Created item with API-fetched details
    """
    try:
        data = request.get_json()
        
        identifier = data.get("identifier")
        search_type = data.get("search_type", "barcode")
        price = data.get("price")
        quantity = data.get("quantity_in_stock")
        
        if not identifier:
            return jsonify({
                "status": "error",
                "message": "Identifier is required"
            }), 400
        
        if price is None or quantity is None:
            return jsonify({
                "status": "error",
                "message": "Price and quantity_in_stock are required"
            }), 400
        
        # Fetch from external API
        api_data = external_api.get_product_details(identifier, search_type)
        
        if not api_data:
            return jsonify({
                "status": "error",
                "message": f"Product not found in external API for {search_type}: {identifier}"
            }), 404
        
        # Format and add to inventory
        if search_type == "barcode":
            item = external_api.format_product_data(api_data)
            item["barcode"] = identifier
        else:
            # For name search, use first result
            item = api_data[0] if isinstance(api_data, list) and api_data else {}
        
        item["price"] = float(price)
        item["quantity_in_stock"] = int(quantity)
        
        created_item = database.add_item(item)
        return jsonify({
            "status": "success",
            "message": "Item created from external API",
            "data": created_item
        }), 201
    except Exception as e:
        logger.error(f"Error creating item from API: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to create item from API"
        }), 500


# ==================== UPDATE OPERATIONS ====================

@api.route("/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    """
    PATCH /inventory/<id>
    Update an existing inventory item
    
    Args:
        item_id (int): The ID of the item to update
        
    JSON Body: Any fields to update
        {
            "price": float,
            "quantity_in_stock": int,
            "status": string,
            ...
        }
        
    Returns:
        JSON: Updated item or error message
    """
    try:
        data = request.get_json()
        
        # Check if item exists
        item = database.get_item_by_id(item_id)
        if not item:
            return jsonify({
                "status": "error",
                "message": f"Item with ID {item_id} not found"
            }), 404
        
        # Update item
        updated_item = database.update_item(item_id, data)
        return jsonify({
            "status": "success",
            "message": "Item updated successfully",
            "data": updated_item
        }), 200
    except Exception as e:
        logger.error(f"Error updating item {item_id}: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to update item"
        }), 500


# ==================== DELETE OPERATIONS ====================

@api.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """
    DELETE /inventory/<id>
    Remove an item from inventory
    
    Args:
        item_id (int): The ID of the item to delete
        
    Returns:
        JSON: Success message or error
    """
    try:
        # Check if item exists
        item = database.get_item_by_id(item_id)
        if not item:
            return jsonify({
                "status": "error",
                "message": f"Item with ID {item_id} not found"
            }), 404
        
        success = database.delete_item(item_id)
        if success:
            return jsonify({
                "status": "success",
                "message": f"Item with ID {item_id} deleted successfully"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to delete item"
            }), 500
    except Exception as e:
        logger.error(f"Error deleting item {item_id}: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to delete item"
        }), 500


# ==================== HELPER ROUTES ====================

@api.route("/stats", methods=["GET"])
def get_stats():
    """
    GET /inventory/stats
    Get inventory statistics
    
    Returns:
        JSON: Inventory statistics
    """
    try:
        items = database.get_all_items()
        
        total_value = sum(item.get("price", 0) * item.get("quantity_in_stock", 0) for item in items)
        total_items = len(items)
        total_quantity = sum(item.get("quantity_in_stock", 0) for item in items)
        
        stats = {
            "total_items": total_items,
            "total_quantity": total_quantity,
            "total_inventory_value": round(total_value, 2),
            "average_item_price": round(total_value / total_items, 2) if total_items > 0 else 0,
            "low_stock_items": [item for item in items if item.get("quantity_in_stock", 0) < 10]
        }
        
        return jsonify({
            "status": "success",
            "message": "Statistics retrieved",
            "data": stats
        }), 200
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve statistics"
        }), 500


@api.route("/reset", methods=["POST"])
def reset_inventory():
    """
    POST /inventory/reset
    Reset inventory to initial state (for testing/development)
    
    Returns:
        JSON: Success message
    """
    try:
        database.reset_database()
        return jsonify({
            "status": "success",
            "message": "Inventory reset to initial state"
        }), 200
    except Exception as e:
        logger.error(f"Error resetting inventory: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to reset inventory"
        }), 500
