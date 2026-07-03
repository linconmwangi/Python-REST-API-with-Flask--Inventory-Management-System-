# Inventory Management System - Flask REST API

A comprehensive Flask-based REST API for managing inventory items with external API integration, CLI interface, and full test coverage.

## 📋 Features

✅ **CRUD Operations** - Create, read, update, and delete inventory items  
✅ **External API Integration** - Fetch real-time product data from OpenFoodFacts API  
✅ **CLI Tool** - User-friendly command-line interface  
✅ **RESTful API** - Fully-featured REST API with proper HTTP methods  
✅ **Unit Tests** - Comprehensive test suite with pytest  
✅ **Error Handling** - Robust error handling and validation  
✅ **Mock Database** - Array-based data storage simulating OpenFoodFacts schema  

## 🏗️ Project Structure

```
inventory-management-system/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── database.py          # Mock database operations
│   ├── routes.py            # API endpoints (CRUD)
│   └── external_api.py      # OpenFoodFacts API integration
├── cli/
│   ├── __init__.py
│   └── main.py              # CLI tool
├── tests/
│   ├── __init__.py
│   └── test_api.py          # Unit tests
├── run.py                   # Application entry point
├── requirements.txt         # Project dependencies
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Setup Steps

1. **Clone the repository**
   ```bash
   cd /path/to/project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**
   ```bash
   python run.py
   ```
   
   Server will start at `http://localhost:5000`

5. **Run tests** (in another terminal with venv activated)
   ```bash
   pytest tests/test_api.py -v
   ```

6. **Run CLI tool** (in another terminal with venv activated)
   ```bash
   python cli/main.py
   ```

## 📡 API Endpoints

### Base URL
```
http://localhost:5000/api/inventory
```

### Endpoints

#### 1. Get All Items
```
GET /api/inventory
```

**Response:**
```json
{
  "status": "success",
  "message": "All inventory items retrieved",
  "count": 3,
  "data": [
    {
      "id": 1,
      "barcode": "5901234123457",
      "product_name": "Organic Almond Milk",
      "brands": "Silk",
      "price": 3.99,
      "quantity_in_stock": 150,
      ...
    }
  ]
}
```

#### 2. Get Single Item
```
GET /api/inventory/<id>
```

**Example:**
```
GET /api/inventory/1
```

**Response:**
```json
{
  "status": "success",
  "message": "Item retrieved",
  "data": {
    "id": 1,
    "barcode": "5901234123457",
    "product_name": "Organic Almond Milk",
    ...
  }
}
```

#### 3. Search Items
```
GET /api/inventory/search?q=<query>&field=<field>
```

**Parameters:**
- `q` (string, required): Search query
- `field` (string, optional): Field to search in (default: product_name)

**Example:**
```
GET /api/inventory/search?q=Almond&field=product_name
```

#### 4. Create Item (Manual)
```
POST /api/inventory
```

**Request Body:**
```json
{
  "product_name": "String (required)",
  "brands": "String (optional)",
  "category": "String (optional)",
  "barcode": "String (optional)",
  "price": "Float (required)",
  "quantity_in_stock": "Integer (required)",
  "unit": "String (optional, default: units)",
  "ingredients_text": "String (optional)",
  "allergens": "String (optional)",
  "status": "String (optional, default: available)"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Coconut Water",
    "brands": "Vita Coco",
    "price": 2.99,
    "quantity_in_stock": 200,
    "category": "Beverages"
  }'
```

#### 5. Create Item from External API
```
POST /api/inventory/from-api
```

**Request Body:**
```json
{
  "identifier": "String (required - barcode or product name)",
  "search_type": "String (required - 'barcode' or 'name')",
  "price": "Float (required)",
  "quantity_in_stock": "Integer (required)"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/inventory/from-api \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "5901234123457",
    "search_type": "barcode",
    "price": 3.99,
    "quantity_in_stock": 100
  }'
```

#### 6. Update Item (PATCH)
```
PATCH /api/inventory/<id>
```

**Request Body:** Any fields to update

**Example:**
```bash
curl -X PATCH http://localhost:5000/api/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 4.99,
    "quantity_in_stock": 175
  }'
```

#### 7. Delete Item
```
DELETE /api/inventory/<id>
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/inventory/1
```

#### 8. Get Inventory Statistics
```
GET /api/inventory/stats
```

**Response:**
```json
{
  "status": "success",
  "message": "Statistics retrieved",
  "data": {
    "total_items": 3,
    "total_quantity": 230,
    "total_inventory_value": 1299.70,
    "average_item_price": 433.23,
    "low_stock_items": []
  }
}
```

#### 9. Reset Inventory
```
POST /api/inventory/reset
```

**Purpose:** Reset inventory to initial state (for testing/development)

## 💻 CLI Tool Usage

Start the CLI tool with:
```bash
python cli/main.py
```

### Menu Options

1. **View all inventory items** - Display all items in table format
2. **View a specific item** - Get details of a single item by ID
3. **Search for items** - Search items by query and field
4. **Add new item (manual)** - Manually add a new inventory item
5. **Add item from external API** - Fetch and add product from OpenFoodFacts
6. **Update item** - Update price or quantity of existing item
7. **Delete item** - Remove item from inventory
8. **View inventory statistics** - Display inventory statistics
9. **Exit** - Close the application

### Example CLI Workflow

```
INVENTORY MANAGEMENT SYSTEM
==================================================
1. View all inventory items
2. View a specific item
3. Search for items
4. Add new item (manual)
5. Add item from external API
6. Update item (price/quantity)
7. Delete item
8. View inventory statistics
9. Exit
==================================================
Enter your choice (1-9): 1

ID    Product Name                   Brand           Price      Stock     
----------------------------------------------------------------------
1     Organic Almond Milk            Silk            $3.99      150       
2     Whole Wheat Bread              Nature's Harvest $2.49     50        
3     Extra Virgin Olive Oil         Colavita        $12.99     30        
```

## 🧪 Testing

Run the complete test suite:
```bash
pytest tests/test_api.py -v
```

Run with coverage report:
```bash
pytest tests/test_api.py -v --cov=app --cov-report=html
```

### Test Coverage

- **Database Operations**: CRUD, search, ID generation
- **API Endpoints**: All GET, POST, PATCH, DELETE operations
- **External API**: Mock data, error handling, data formatting
- **Error Cases**: Missing fields, invalid data, non-existent items
- **Statistics**: Inventory stats calculations

Example test output:
```
tests/test_api.py::TestDatabaseOperations::test_get_all_items PASSED
tests/test_api.py::TestDatabaseOperations::test_add_item PASSED
tests/test_api.py::TestDatabaseOperations::test_delete_item PASSED
tests/test_api.py::TestFlaskAPI::test_get_all_items PASSED
tests/test_api.py::TestFlaskAPI::test_create_item PASSED
tests/test_api.py::TestFlaskAPI::test_delete_item PASSED
...
```

## 📊 Database Schema

### Item Structure

```json
{
  "id": "Integer (auto-generated)",
  "barcode": "String",
  "product_name": "String",
  "brands": "String",
  "category": "String",
  "ingredients_text": "String",
  "price": "Float",
  "quantity_in_stock": "Integer",
  "unit": "String",
  "nutrient_levels": {
    "energy": "String",
    "fat": "String",
    "carbohydrates": "String",
    "protein": "String"
  },
  "allergens": "String",
  "status": "String (available/discontinued/out_of_stock)"
}
```

## 🔌 External API Integration

### OpenFoodFacts API

The system integrates with the OpenFoodFacts API to fetch real product data:

**API Base URL:** `https://world.openfoodfacts.org/api/v0/product`

**Features:**
- Search by barcode
- Search by product name
- Fetch nutrient information
- Get allergen data
- Extract ingredients information

**Mock Data:**
The system includes mock data for testing to avoid excessive API calls:
- Barcode: 5901234123457 - Organic Almond Milk
- Barcode: 5901234123458 - Whole Wheat Bread

## 📝 API Response Format

All responses follow a consistent format:

### Success Response (2xx)
```json
{
  "status": "success",
  "message": "Operation description",
  "data": { /* response data */ },
  "count": 0  /* if applicable */
}
```

### Error Response (4xx, 5xx)
```json
{
  "status": "error",
  "message": "Error description"
}
```

## 🛠️ Development

### Adding New Endpoints

1. Add function to `app/routes.py`
2. Use appropriate HTTP method (GET, POST, PATCH, DELETE)
3. Add docstring with endpoint details
4. Add unit tests in `tests/test_api.py`

Example:
```python
@api.route("/custom", methods=["GET"])
def custom_endpoint():
    """
    GET /api/inventory/custom
    Custom endpoint description
    """
    try:
        # Implementation
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": "Error message"}), 500
```

### Database Modifications

All database operations are in `app/database.py`. The mock database uses a global `inventory_db` list:

```python
# Example: Adding a new search function
def search_by_category(category):
    """Search items by category"""
    return [item for item in inventory_db if item.get("category") == category]
```

## 🐛 Debugging

### Enable Debug Mode

The Flask app runs in debug mode by default. View real-time updates in the console:

```python
app.run(debug=True)  # In run.py
```

### View Logs

Application logs appear in the console output. Set log level in `app/__init__.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # More verbose logging
```

### Test with Postman

1. Import API endpoints into Postman
2. Test each endpoint with different payloads
3. Verify response status codes and data
4. Check error handling

## 🚀 Deployment

To run in production:

1. Update `run.py`:
```python
app.run(debug=False, host="0.0.0.0", port=5000)
```

2. Use production WSGI server (Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 📦 Dependencies

- **Flask 2.3.2** - Web framework
- **Flask-CORS 4.0.0** - Cross-origin requests
- **requests 2.31.0** - HTTP library for external API
- **pytest 7.4.0** - Testing framework
- **pytest-cov 4.1.0** - Test coverage
- **python-dotenv 1.0.0** - Environment variables

## 📄 License

This project is created as a Summative Lab assignment.

## 👨‍💻 Author

Created as part of Moringa School curriculum - Summative Lab 01

## 📞 Support

For issues or questions:
1. Check existing GitHub issues
2. Review API documentation
3. Run tests to verify functionality
4. Check console logs for errors

## 🎯 Requirements Met

✅ Flask Routing - All CRUD routes and helper routes implemented  
✅ CRUD Operations - Full Read, Create, Update, Delete functionality  
✅ External API - OpenFoodFacts integration with UI to fetch and add items  
✅ Git Management - Repository with branches and organized commits  
✅ Testing - Comprehensive unit tests with pytest and mock objects  

---

**Last Updated:** 2026-07-03  
**Version:** 1.0.0
