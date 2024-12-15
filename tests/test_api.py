import pytest
from app import create_app

def test_get_products(client):
    response = client.get('/products/')
    print(response)
    assert response.status_code == 200

def test_create_product(client):
    product_data = {
        'name': 'API Product',
        'price': 25.0,
        'stock': 30
    }
    response = client.post('/products/', json=product_data)
    print(response)
    assert response.status_code == 201

def test_place_order(client):
    # test_create_product(client)
    order_data = {
        'products': [{'product_id': 1, 'quantity': 2}]
    }
    response = client.post('/orders/', json=order_data)
    assert response.status_code == 201 