# Quick Start Guide

## 🚀 Getting Started Quickly

### 1. Setup Python Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Flask Server
```bash
python3 run.py
```
Server will start at `http://localhost:5000`

### 3. Test the API (in another terminal)
```bash
# Get all items
curl http://localhost:5000/api/inventory

# Check health
curl http://localhost:5000/health

# Get statistics
curl http://localhost:5000/api/inventory/stats
```

### 4. Run Unit Tests (in another terminal with venv)
```bash
pytest tests/test_api.py -v
```

### 5. Run CLI Tool (in another terminal with venv)
```bash
python3 cli/main.py
```

## 📝 Example API Calls

### Create Item
```bash
curl -X POST http://localhost:5000/api/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Coconut Water",
    "brands": "Vita Coco",
    "price": 2.99,
    "quantity_in_stock": 200
  }'
```

### Get Item by ID
```bash
curl http://localhost:5000/api/inventory/1
```

### Update Item
```bash
curl -X PATCH http://localhost:5000/api/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 4.99}'
```

### Delete Item
```bash
curl -X DELETE http://localhost:5000/api/inventory/1
```

### Search Items
```bash
curl 'http://localhost:5000/api/inventory/search?q=Almond&field=product_name'
```

## 🧪 Test Results

All 36 unit tests passing:
- ✅ 12 Database operation tests
- ✅ 15 Flask API endpoint tests
- ✅ 6 External API integration tests
- ✅ 3 API creation from external source tests

Run tests with coverage:
```bash
pytest tests/test_api.py -v --cov=app --cov-report=html
```

## 📚 Project Structure

```
app/
  ├── __init__.py         # Flask app factory
  ├── database.py         # Mock database
  ├── routes.py           # API endpoints
  └── external_api.py     # OpenFoodFacts integration
cli/
  └── main.py             # CLI tool
tests/
  └── test_api.py         # Unit tests
```

## 🔄 Git Branches

- `feature/database` - Mock database implementation
- `feature/external-api` - OpenFoodFacts API integration
- `feature/api-routes` - Flask CRUD endpoints
- `feature/cli-tool` - CLI interface
- `feature/testing` - Unit tests
- `feature/documentation` - README and docs
- `setup/project-config` - Dependencies and configuration
- `main` - Merged main branch

## 🆘 Troubleshooting

**"Cannot connect to API server"**
- Ensure Flask server is running: `python3 run.py`
- Check if port 5000 is available

**"Test failures with werkzeug"**
- Update dependencies: `pip install --upgrade Flask Werkzeug`

**"CLI cannot connect"**
- Make sure Flask server is running in another terminal
- Check host/port in `cli/main.py`

## 📖 Full Documentation

See [README.md](README.md) for complete API documentation and advanced usage.
