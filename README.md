# E-Commerce Platform RESTful API

## Overview
This is a production-grade RESTful API for an e-commerce platform built with Flask, SQLAlchemy, MySQL. The application provides endpoints for managing products and orders with robust stock management and caching mechanisms.

## System Architecture
- **Backend**: Python Flask
- **Database**: MySQL
- **Containerization**: Docker, Docker Compose

## Features
- Product management
- Order placement with stock validation
- Comprehensive error handling
- Dockerized deployment
- Comprehensive test suite

## Prerequisites
- Docker
- Docker Compose
- Git
- Python

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/justinjoy07/ecommerce-api.git
cd ecommerce-api
```


### 2. Build and Run
```bash
docker-compose up --build
```

The API will be available at `http://localhost:5002`

## API Endpoints

### Products
- `GET /products`
  - Retrieves all available products
  - Query Parameters:
    - `page`: The page number to retrieve (default is 1)
    - `per_page`: Number of products per page (default is 10)
  - Returns: List of product objects

- `POST /products`
  - Add a new product
  - Request Body:
    ```json
    {
      "name": "Product Name",
      "description": "Product Description",
      "price": 19.99,
      "stock": 100
    }
    ```

### Orders
- `POST /orders`
  - Place a new order
  - Validates product stock before order confirmation
  - Request Body:
    ```json
    {
      "products": [
        {
          "product_id": 1,
          "quantity": 2
        }
      ]
    }
    ```

## Testing
Navigate to the project directory:
```bash
cd /path/to/the/project
```
Create the virtual environment:
```bash
python3 -m venv venv
```
Activate the virtual environment:
```bash
source venv/bin/activate
```
Install Requirements
```bash
pip install -r requirements.txt
```
Run tests:
```bash
TESTING_MODE=TRUE pytest -v
```

## Error Handling
- Comprehensive error responses for:
  - Insufficient stock
  - Invalid product data
  - Order validation failures


## Security Considerations
- Input validation
- Exception handling
- Separate environments for development and production
