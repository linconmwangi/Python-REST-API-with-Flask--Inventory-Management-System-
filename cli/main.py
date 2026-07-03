"""
CLI Tool for Inventory Management System
Command-line interface to interact with the API
"""

import requests
import json
import sys
from typing import Optional, Dict, Any

# API base URL
API_BASE_URL = "http://localhost:5000/api/inventory"


class InventoryClient:
    """Client for interacting with the Inventory Management API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        """Initialize the client with base URL"""
        self.base_url = base_url
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API responses"""
        try:
            return response.json()
        except:
            return {"status": "error", "message": "Failed to parse response"}
    
    # ==================== READ OPERATIONS ====================
    
    def get_all_items(self):
        """Fetch all inventory items"""
        try:
            response = requests.get(f"{self.base_url}")
            return self._handle_response(response)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_item(self, item_id: int):
        """Fetch a single item by ID"""
        try:
            response = requests.get(f"{self.base_url}/{item_id}")
            return self._handle_response(response)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def search_items(self, query: str, field: str = "product_name"):
        """Search items"""
        try:
            response = requests.get(
                f"{self.base_url}/search",
                params={"q": query, "field": field}
            )
            return self._handle_response(response)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ==================== CREATE OPERATIONS ====================
    
    def create_item(self, item_data: Dict[str, Any]):
        """Create a new item"""
        try:
            response = requests.post(f"{self.base_url}", json=item_data)
            return self._handle_response(response)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_item_from_api(self, identifier: str, search_type: str, 
                            price: float, quantity: int):
        """Create item from external API"""
        try:
            data = {
                "identifier": identifier,
                "search_type": search_type,
                "price": price,
                "quantity_in_stock": quantity
            }
            response = requests.post(f"{self.base_url}/from-api", json=data)
            return self._handle_response(response)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ==================== UPDATE OPERATIONS ====================
    
    def update_item(self, item_id: int, update_data: Dict[str, Any]):
        """Update an item"""
        try:
            response = requests.patch(f"{self.base_url}/{item_id}", json=update_data)
            return self._handle_response(response)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ==================== DELETE OPERATIONS ====================
    
    def delete_item(self, item_id: int):
        """Delete an item"""
        try:
            response = requests.delete(f"{self.base_url}/{item_id}")
            return self._handle_response(response)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ==================== STATS ====================
    
    def get_stats(self):
        """Get inventory statistics"""
        try:
            response = requests.get(f"{self.base_url}/stats")
            return self._handle_response(response)
        except Exception as e:
            return {"status": "error", "message": str(e)}


def print_menu():
    """Display the CLI menu"""
    print("\n" + "="*50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. View all inventory items")
    print("2. View a specific item")
    print("3. Search for items")
    print("4. Add new item (manual)")
    print("5. Add item from external API")
    print("6. Update item (price/quantity)")
    print("7. Delete item")
    print("8. View inventory statistics")
    print("9. Exit")
    print("="*50)


def get_valid_input(prompt: str, input_type=str, allow_empty=False):
    """Get validated user input"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and not allow_empty:
                print("Input cannot be empty. Please try again.")
                continue
            if input_type == int:
                return int(user_input)
            elif input_type == float:
                return float(user_input)
            else:
                return user_input
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)


def view_all_items(client: InventoryClient):
    """Display all inventory items"""
    print("\nFetching all items...")
    result = client.get_all_items()
    
    if result.get("status") == "success":
        items = result.get("data", [])
        if not items:
            print("No items in inventory.")
        else:
            print(f"\n{'ID':<5} {'Product Name':<30} {'Brand':<15} {'Price':<10} {'Stock':<10}")
            print("-" * 70)
            for item in items:
                print(f"{item['id']:<5} {item['product_name']:<30} {item['brands']:<15} "
                      f"${item['price']:<9.2f} {item['quantity_in_stock']:<10}")
    else:
        print(f"Error: {result.get('message')}")


def view_item(client: InventoryClient):
    """Display a specific item"""
    item_id = get_valid_input("Enter item ID: ", int)
    result = client.get_item(item_id)
    
    if result.get("status") == "success":
        item = result.get("data", {})
        print("\n" + json.dumps(item, indent=2))
    else:
        print(f"Error: {result.get('message')}")


def search_items(client: InventoryClient):
    """Search for items"""
    query = get_valid_input("Enter search query: ")
    field = input("Enter field to search in (default: product_name): ").strip() or "product_name"
    
    result = client.search_items(query, field)
    
    if result.get("status") == "success":
        items = result.get("data", [])
        if not items:
            print("No items found.")
        else:
            print(f"\nFound {len(items)} item(s):")
            print(f"\n{'ID':<5} {'Product Name':<30} {'Brand':<15} {'Price':<10} {'Stock':<10}")
            print("-" * 70)
            for item in items:
                print(f"{item['id']:<5} {item['product_name']:<30} {item['brands']:<15} "
                      f"${item['price']:<9.2f} {item['quantity_in_stock']:<10}")
    else:
        print(f"Error: {result.get('message')}")


def add_item_manual(client: InventoryClient):
    """Add a new item manually"""
    print("\nAdd New Item")
    
    item_data = {
        "product_name": get_valid_input("Product name: "),
        "brands": get_valid_input("Brand: ", allow_empty=True),
        "category": get_valid_input("Category (default: General): ", allow_empty=True) or "General",
        "barcode": get_valid_input("Barcode (optional): ", allow_empty=True),
        "ingredients_text": get_valid_input("Ingredients (optional): ", allow_empty=True),
        "price": get_valid_input("Price: ", float),
        "quantity_in_stock": get_valid_input("Quantity in stock: ", int),
        "unit": get_valid_input("Unit (default: units): ", allow_empty=True) or "units",
        "status": get_valid_input("Status (default: available): ", allow_empty=True) or "available"
    }
    
    result = client.create_item(item_data)
    
    if result.get("status") == "success":
        print(f"\nItem created successfully!")
        print(f"Item ID: {result['data']['id']}")
    else:
        print(f"Error: {result.get('message')}")


def add_item_from_api(client: InventoryClient):
    """Add item from external API"""
    print("\nAdd Item from External API")
    
    search_type = input("Search by (barcode/name): ").strip().lower()
    if search_type not in ["barcode", "name"]:
        print("Invalid search type. Must be 'barcode' or 'name'.")
        return
    
    identifier = get_valid_input(f"Enter {search_type}: ")
    price = get_valid_input("Price: ", float)
    quantity = get_valid_input("Quantity: ", int)
    
    print("\nFetching from external API...")
    result = client.create_item_from_api(identifier, search_type, price, quantity)
    
    if result.get("status") == "success":
        print(f"\nItem created successfully from API!")
        print(f"Item ID: {result['data']['id']}")
        print(f"Product: {result['data'].get('product_name')}")
    else:
        print(f"Error: {result.get('message')}")


def update_item(client: InventoryClient):
    """Update item price or quantity"""
    item_id = get_valid_input("Enter item ID to update: ", int)
    
    print("\nWhat would you like to update?")
    print("1. Price")
    print("2. Quantity")
    print("3. Both")
    
    choice = get_valid_input("Enter choice (1-3): ")
    
    update_data = {}
    
    if choice in ["1", "3"]:
        update_data["price"] = get_valid_input("New price: ", float)
    
    if choice in ["2", "3"]:
        update_data["quantity_in_stock"] = get_valid_input("New quantity: ", int)
    
    if not update_data:
        print("No updates provided.")
        return
    
    result = client.update_item(item_id, update_data)
    
    if result.get("status") == "success":
        print(f"\nItem updated successfully!")
        print(json.dumps(result['data'], indent=2))
    else:
        print(f"Error: {result.get('message')}")


def delete_item(client: InventoryClient):
    """Delete an item"""
    item_id = get_valid_input("Enter item ID to delete: ", int)
    
    confirm = input(f"Are you sure you want to delete item {item_id}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return
    
    result = client.delete_item(item_id)
    
    if result.get("status") == "success":
        print(f"\nItem deleted successfully!")
    else:
        print(f"Error: {result.get('message')}")


def view_stats(client: InventoryClient):
    """Display inventory statistics"""
    print("\nFetching inventory statistics...")
    result = client.get_stats()
    
    if result.get("status") == "success":
        stats = result.get("data", {})
        print("\n" + "="*50)
        print("INVENTORY STATISTICS")
        print("="*50)
        print(f"Total Items: {stats.get('total_items')}")
        print(f"Total Quantity: {stats.get('total_quantity')}")
        print(f"Total Inventory Value: ${stats.get('total_inventory_value', 0):.2f}")
        print(f"Average Item Price: ${stats.get('average_item_price', 0):.2f}")
        
        low_stock = stats.get('low_stock_items', [])
        if low_stock:
            print(f"\nLow Stock Items ({len(low_stock)}):")
            for item in low_stock:
                print(f"  - {item['product_name']}: {item['quantity_in_stock']} units")
        else:
            print("\nNo low stock items.")
    else:
        print(f"Error: {result.get('message')}")


def main():
    """Main CLI application loop"""
    client = InventoryClient()
    
    print("\nStarting Inventory Management CLI...")
    print("Make sure the Flask server is running on http://localhost:5000")
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✓ Connected to API server")
        else:
            print("✗ Unable to connect to API server")
            sys.exit(1)
    except:
        print("✗ Cannot connect to API server at http://localhost:5000")
        print("Please start the Flask server first: python run.py")
        sys.exit(1)
    
    # Main loop
    while True:
        print_menu()
        choice = get_valid_input("Enter your choice (1-9): ")
        
        if choice == "1":
            view_all_items(client)
        elif choice == "2":
            view_item(client)
        elif choice == "3":
            search_items(client)
        elif choice == "4":
            add_item_manual(client)
        elif choice == "5":
            add_item_from_api(client)
        elif choice == "6":
            update_item(client)
        elif choice == "7":
            delete_item(client)
        elif choice == "8":
            view_stats(client)
        elif choice == "9":
            print("\nThank you for using Inventory Management System. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
