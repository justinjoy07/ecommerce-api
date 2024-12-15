from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import JSON

Base = declarative_base()

class Product(Base):
    """
    Product model representing available items in the e-commerce platform.
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    price = Column(Float(precision=2), nullable=False)
    stock = Column(Integer, nullable=False)

    def to_dict(self):
        """
        Convert product to dictionary representation.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock
        }

class Order(Base):
    """
    Order model representing customer purchase transactions.
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    products = Column(JSON, nullable=False)  # Store product IDs and quantities
    total_price = Column(Float(precision=2), nullable=False)
    status = Column(String(50), nullable=False, default='pending')

    def to_dict(self):
        """
        Convert order to dictionary representation.
        """
        return {
            'id': self.id,
            'products': self.products,
            'total_price': self.total_price,
            'status': self.status
        }
    