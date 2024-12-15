from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.services import ProductService, OrderService
from app.exceptions import InsufficientStockError, ProductValidationError

def init_routes(app, session: Session):
    products_bp = Blueprint('products', __name__, url_prefix="/products")
    orders_bp = Blueprint('orders', __name__, url_prefix="/orders")

    @products_bp.route('/', methods=['GET'])
    def get_products():
        """
        Retrieve all available products.
        """
        try:
            # Get pagination parameters from the request
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            product_service = ProductService(session)
            products = product_service.get_all_products(page=page, per_page=per_page)
            return jsonify(products), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @products_bp.route('/', methods=['POST'])
    def create_product():
        """
        Add a new product to the platform.
        """
        try:
            product_data = request.json
            product_service = ProductService(session)
            new_product = product_service.add_product(product_data)
            return jsonify(new_product.to_dict()), 201
        except ProductValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @orders_bp.route('/', methods=['POST'])
    def place_order():
        """
        Place an order for selected products.
        """
        try:
            order_data = request.json.get('products', [])
            order_service = OrderService(session)
            order = order_service.place_order(order_data)
            return jsonify(order.to_dict()), 201
        except InsufficientStockError as e:
            return jsonify({
                'error': 'Insufficient Stock',
                'details': {
                    'product_id': e.product_id,
                    'requested': e.requested_quantity,
                    'available': e.available_stock
                }
            }), 400
        except ProductValidationError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Register blueprints
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)