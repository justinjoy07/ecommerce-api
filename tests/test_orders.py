import pytest
from app.services import OrderService
from app.models import Product
from app.exceptions import InsufficientStockError, ProductValidationError

class TestOrderService:
    def test_place_order_success(self, session):
        # Setup: Create a product first
        product = Product(name='Test Product', price=10.0, stock=50)
        session.add(product)
        session.commit()

        order_service = OrderService(session)
        order_products = [
            {
                'product_id': product.id,
                'quantity': 5
            }
        ]
        
        order = order_service.place_order(order_products)
        
        assert order.total_price == 50.0
        assert order.status == 'completed'
        
        # Verify stock reduction
        updated_product = session.get(Product, product.id)
        assert updated_product.stock == 45

    def test_place_order_insufficient_stock(self, session):
        # Setup: Create a product first
        product = Product(name='Test Product', price=10.0, stock=5)
        session.add(product)
        session.commit()

        order_service = OrderService(session)
        order_products = [
            {
                'product_id': product.id,
                'quantity': 10
            }
        ]
        
        with pytest.raises(InsufficientStockError):
            order_service.place_order(order_products)