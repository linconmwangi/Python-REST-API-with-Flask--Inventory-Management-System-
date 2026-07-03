"""Unit Tests for Inventory Management System"""

import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock
from app import create_app, database
from app import external_api


class TestDatabaseOperations:
    """Test database CRUD operations"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset database before each test"""
        database.reset_database()
        yield
        database.reset_database()
    
    def test_get_all_items(self):
        """Test retrieving all items"""
        items = database.get_all_items()
        assert len(items) == 3
        assert items[0]["product_name"] == "Organic Almond Milk"
    
    def test_get_item_by_id(self):
        """Test retrieving single item by ID"""
        item = database.get_item_by_id(1)
        assert item is not None
        assert item["product_name"] == "Organic Almond Milk"
        assert item["id"] == 1
    
    def test_get_item_by_id_not_found(self):
        """Test retrieving non-existent item"""
        item = database.get_item_by_id(999)
        assert item is None
    
    def test_add_item(self):
        """Test adding a new item"""
        new_item = {
            "product_name": "Test Product",
            "brands": "Test Brand",
            "price": 9.99,
            "quantity_in_stock": 50,
            "category": "Test"
        }
        created = database.add_item(new_item)
        assert created["id"] == 4
        assert created["product_name"] == "Test Product"
        
        # Verify it was added
        items = database.get_all_items()
        assert len(items) == 4
    
    def test_update_item(self):
        """Test updating an item"""
        updated = database.update_item(1, {"price": 5.99, "quantity_in_stock": 200})
        assert updated["price"] == 5.99
        assert updated["quantity_in_stock"] == 200
        
        # Verify update persisted
        item = database.get_item_by_id(1)
        assert item["price"] == 5.99
    
    def test_update_nonexistent_item(self):
        """Test updating non-existent item"""
        result = database.update_item(999, {"price": 5.99})
        assert result is None
    
    def test_delete_item(self):
        """Test deleting an item"""
        success = database.delete_item(1)
        assert success is True
        
        # Verify deletion
        item = database.get_item_by_id(1)
        assert item is None
        
        items = database.get_all_items()
        assert len(items) == 2
    
    def test_delete_nonexistent_item(self):
        """Test deleting non-existent item"""
        success = database.delete_item(999)
        assert success is False
    
    def test_search_items_by_name(self):
        """Test searching items by product name"""
        results = database.search_items("Almond", "product_name")
        assert len(results) == 1
        assert results[0]["product_name"] == "Organic Almond Milk"
    
    def test_search_items_by_brand(self):
        """Test searching items by brand"""
        results = database.search_items("Silk", "brands")
        assert len(results) == 1
        assert results[0]["brands"] == "Silk"
    
    def test_search_no_results(self):
        """Test search with no results"""
        results = database.search_items("NonExistent", "product_name")
        assert len(results) == 0
    
    def test_get_next_id(self):
        """Test ID generation"""
        next_id = database.get_next_id()
        assert next_id == 4


class TestFlaskAPI:
    """Test Flask API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app = create_app({"TESTING": True})
        app.config["TESTING"] = True
        
        with app.app_context():
            database.reset_database()
            yield app.test_client()
            database.reset_database()
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"
    
    def test_get_all_items(self, client):
        """Test GET /api/inventory"""
        response = client.get("/api/inventory")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["count"] == 3
        assert len(data["data"]) == 3
    
    def test_get_single_item(self, client):
        """Test GET /api/inventory/<id>"""
        response = client.get("/api/inventory/1")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["data"]["product_name"] == "Organic Almond Milk"
    
    def test_get_nonexistent_item(self, client):
        """Test GET /api/inventory/<id> for non-existent item"""
        response = client.get("/api/inventory/999")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["status"] == "error"
    
    def test_search_items(self, client):
        """Test GET /api/inventory/search"""
        response = client.get("/api/inventory/search?q=Almond")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["count"] == 1
    
    def test_search_no_query(self, client):
        """Test search without query parameter"""
        response = client.get("/api/inventory/search")
        assert response.status_code == 400
    
    def test_create_item(self, client):
        """Test POST /api/inventory"""
        item_data = {
            "product_name": "New Product",
            "brands": "New Brand",
            "price": 7.99,
            "quantity_in_stock": 100,
            "category": "Test"
        }
        response = client.post("/api/inventory", json=item_data)
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["data"]["id"] == 4
        assert data["data"]["product_name"] == "New Product"
    
    def test_create_item_missing_required_field(self, client):
        """Test POST /api/inventory with missing required field"""
        item_data = {
            "product_name": "New Product",
            "brands": "New Brand"
            # Missing price and quantity_in_stock
        }
        response = client.post("/api/inventory", json=item_data)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["status"] == "error"
    
    def test_create_item_invalid_price(self, client):
        """Test POST /api/inventory with invalid price"""
        item_data = {
            "product_name": "New Product",
            "price": "invalid",
            "quantity_in_stock": 100
        }
        response = client.post("/api/inventory", json=item_data)
        assert response.status_code == 400
    
    def test_update_item(self, client):
        """Test PATCH /api/inventory/<id>"""
        update_data = {
            "price": 5.99,
            "quantity_in_stock": 200
        }
        response = client.patch("/api/inventory/1", json=update_data)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["data"]["price"] == 5.99
        assert data["data"]["quantity_in_stock"] == 200
    
    def test_update_nonexistent_item(self, client):
        """Test PATCH /api/inventory/<id> for non-existent item"""
        update_data = {"price": 5.99}
        response = client.patch("/api/inventory/999", json=update_data)
        assert response.status_code == 404
    
    def test_delete_item(self, client):
        """Test DELETE /api/inventory/<id>"""
        response = client.delete("/api/inventory/1")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        
        # Verify deletion
        response = client.get("/api/inventory/1")
        assert response.status_code == 404
    
    def test_delete_nonexistent_item(self, client):
        """Test DELETE /api/inventory/<id> for non-existent item"""
        response = client.delete("/api/inventory/999")
        assert response.status_code == 404
    
    def test_get_stats(self, client):
        """Test GET /api/inventory/stats"""
        response = client.get("/api/inventory/stats")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        stats = data["data"]
        assert stats["total_items"] == 3
        assert "total_inventory_value" in stats
        assert "average_item_price" in stats
    
    def test_reset_inventory(self, client):
        """Test POST /api/inventory/reset"""
        # Delete an item first
        client.delete("/api/inventory/1")
        
        # Verify it's gone
        response = client.get("/api/inventory")
        data = json.loads(response.data)
        assert data["count"] == 2
        
        # Reset
        response = client.post("/api/inventory/reset")
        assert response.status_code == 200
        
        # Verify all items are back
        response = client.get("/api/inventory")
        data = json.loads(response.data)
        assert data["count"] == 3


class TestExternalAPI:
    """Test external API integration"""
    
    def test_fetch_product_by_barcode_mock(self):
        """Test fetching product by barcode with mock data"""
        result = external_api.fetch_product_by_barcode("5901234123457")
        assert result is not None
        assert result["status"] == 1
        assert result["product"]["product_name"] == "Organic Almond Milk"
    
    def test_fetch_product_by_barcode_not_found(self):
        """Test fetching non-existent barcode"""
        result = external_api.fetch_product_by_barcode("000000000000")
        # Should fail gracefully (returns None or API error)
        assert result is None or result.get("status") != 1
    
    @patch('app.external_api.requests.get')
    def test_fetch_product_api_error(self, mock_get):
        """Test handling of API errors"""
        mock_get.side_effect = Exception("Connection error")
        result = external_api.fetch_product_by_barcode("999999999999")
        assert result is None
    
    def test_format_product_data(self):
        """Test formatting product data"""
        api_response = {
            "product": {
                "product_name": "Test Product",
                "brands": "Test Brand",
                "code": "123456"
            }
        }
        formatted = external_api.format_product_data(api_response)
        assert formatted["product_name"] == "Test Product"
        assert formatted["brands"] == "Test Brand"
        assert formatted["barcode"] == "123456"
    
    def test_get_product_details_barcode(self):
        """Test get_product_details with barcode search"""
        result = external_api.get_product_details("5901234123457", "barcode")
        assert result is not None
        assert result["status"] == 1
    
    def test_get_product_details_invalid_type(self):
        """Test get_product_details with invalid search type"""
        result = external_api.get_product_details("test", "invalid")
        assert result is None


class TestCreateItemFromAPI:
    """Test creating items from external API"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app = create_app({"TESTING": True})
        app.config["TESTING"] = True
        
        with app.app_context():
            database.reset_database()
            yield app.test_client()
            database.reset_database()
    
    def test_create_item_from_api_barcode(self, client):
        """Test creating item from API with barcode"""
        data = {
            "identifier": "5901234123457",
            "search_type": "barcode",
            "price": 3.99,
            "quantity_in_stock": 100
        }
        response = client.post("/api/inventory/from-api", json=data)
        assert response.status_code == 201
        result = json.loads(response.data)
        assert result["status"] == "success"
        assert result["data"]["product_name"] == "Organic Almond Milk"
    
    def test_create_item_from_api_missing_identifier(self, client):
        """Test creating item from API without identifier"""
        data = {
            "search_type": "barcode",
            "price": 3.99,
            "quantity_in_stock": 100
        }
        response = client.post("/api/inventory/from-api", json=data)
        assert response.status_code == 400
    
    def test_create_item_from_api_missing_price(self, client):
        """Test creating item from API without price"""
        data = {
            "identifier": "5901234123457",
            "search_type": "barcode",
            "quantity_in_stock": 100
        }
        response = client.post("/api/inventory/from-api", json=data)
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
