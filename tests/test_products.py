import pytest
from app.services import ProductService
from app.models import Product
from app.exceptions import ProductValidationError

class TestProductService:
    def test_add_product_success(self, session):
        product_service = ProductService(session)
        product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 19.99,
            'stock': 100
        }
        
        product = product_service.add_product(product_data)
        
        assert product.name == 'Test Product'
        assert product.price == 19.99
        assert product.stock == 100

    def test_add_product_invalid_price(self, session):
        product_service = ProductService(session)
        product_data = {
            'name': 'Invalid Product',
            'price': -10
        }
        
        with pytest.raises(ProductValidationError):
            product_service.add_product(product_data)