from app.models import Product, Order
from app.exceptions import InsufficientStockError, ProductValidationError
from sqlalchemy.orm import Session
from typing import List, Dict

class ProductService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_products(self, page: int = 1, per_page: int = 10) -> List[Product]:
        """
        Retrieve all available products with pagination.
        
        Args:
            page: The page number to retrieve (1-based indexing)
            per_page: Number of items per page
            
        Returns:
            List of products for the requested page
        """

        total_count = self.session.query(Product).count()
        products = self.session.query(Product)\
            .offset((page - 1) * per_page)\
            .limit(per_page)\
            .all()
        
        response = {
        'products': [product.to_dict() for product in products],
        'total':total_count,
        'current_page': page,
        'per_page': per_page
    }

        return response

    def add_product(self, product_data: Dict) -> Product:
        """
        Add a new product with validation.
        """
        # Validate product data
        if not product_data.get('name') or  len(product_data.get("name")) > 255:
            raise ProductValidationError("Product name is required and should be less than 255 characters")
        if product_data.get('price', 0) <= 0 and isinstance(product_data.get('price'), (int, float)):
            raise ProductValidationError("Price must be positive number")
        if not isinstance(product_data.get('stock'), (int)) or product_data.get('stock') < 0:
            raise ProductValidationError("Stock must be a positive integer")
        
        existing_product = self.session.query(Product).filter_by(name=product_data['name']).first()
        if existing_product:
            raise ProductValidationError("Product with this name already exists")
        
        
        new_product = Product(
            name=product_data['name'],
            description=product_data.get('description', ''),
            price=product_data['price'],
            stock=product_data.get('stock', 0)
        )
        
        self.session.add(new_product)
        self.session.commit()
        return new_product

class OrderService:
    def __init__(self, session: Session):
        self.session = session

    def place_order(self, order_products: List[Dict]) -> Order:
        """
        Place an order with stock validation.
        """
        total_price = 0
        order_details = []

        # Validate stock
        for item in order_products:
            product = self.session.get(Product, item['product_id'])
            
            if not product:
                raise ProductValidationError(f"Product {item['product_id']} not found")
            
            if product.stock < item['quantity']:
                raise InsufficientStockError(
                    product_id=product.id, 
                    requested_quantity=item['quantity'], 
                    available_stock=product.stock
                )
            
            total_price += product.price * item['quantity']
            order_details.append({
                'product_id': product.id,
                'quantity': item['quantity'],
                'price': product.price
            })

        # Update stock
        for item in order_products:
            product = self.session.get(Product, item['product_id'])
            product.stock -= item['quantity']

        # Create order
        order = Order(
            products=order_details,
            total_price=total_price,
            status='completed'
        )
        
        self.session.add(order)
        self.session.commit()
        return order