# Inventory Management System - Flask REST API

A Flask-based REST API for managing inventory items, with external API integration, a CLI tool, and full test coverage.

## Features

- CRUD operations for inventory items
- External API integration (OpenFoodFacts) for real-time product data
- CLI tool for managing inventory from the terminal
- RESTful design with proper HTTP methods
- Unit tests with pytest
- Robust error handling and validation
- Mock database (array-based, simulating OpenFoodFacts schema)

## Project Structure

```
inventory-management-system/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── database.py          # Mock database operations
│   ├── routes.py            # API endpoints (CRUD)
│   └── external_api.py      # OpenFoodFacts API integration
├── cli/
│   └── main.py              # CLI tool
├── tests/
│   └── test_api.py          # Unit tests
├── run.py                   # Application entry point
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py                 # starts server at http://localhost:5000
```

Run tests (separate terminal, venv active):
```bash
pytest tests/test_api.py -v
```

Run CLI tool (separate terminal, venv active):
```bash
python cli/main.py
```

## API Endpoints

Base URL: `http://localhost:5000/api/inventory`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Get all items |
| GET | `/<id>` | Get a single item |
| GET | `/search?q=<query>&field=<field>` | Search items |
| POST | `/` | Create item manually |
| POST | `/from-api` | Create item from OpenFoodFacts data |
| PATCH | `/<id>` | Update an item |
| DELETE | `/<id>` | Delete an item |
| GET | `/stats` | Get inventory statistics |
| POST | `/reset` | Reset inventory to initial state |

**Example — create item:**
```bash
curl -X POST http://localhost:5000/api/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Coconut Water", "price": 2.99, "quantity_in_stock": 200}'
```

**Response format:**
```json
{
  "status": "success",
  "message": "Description",
  "data": { }
}
```

## CLI Tool

Run `python cli/main.py` for a menu-driven interface to view, search, add, update, delete items, fetch from the external API, and view stats.

## Database Schema

```json
{
  "id": "Integer (auto-generated)",
  "barcode": "String",
  "product_name": "String",
  "brands": "String",
  "category": "String",
  "price": "Float",
  "quantity_in_stock": "Integer",
  "unit": "String",
  "nutrient_levels": { "energy": "String", "fat": "String", "carbohydrates": "String", "protein": "String" },
  "allergens": "String",
  "status": "String (available/discontinued/out_of_stock)"
}
```

## External API Integration

Uses the OpenFoodFacts API (`https://world.openfoodfacts.org/api/v0/product`) to fetch product data by barcode or name, including nutrients, allergens, and ingredients. Mock data is included for two barcodes to limit live API calls during testing.

## Deployment

```python
app.run(debug=False, host="0.0.0.0", port=5000)
```

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Dependencies

Flask, Flask-CORS, requests, pytest, pytest-cov, python-dotenv

