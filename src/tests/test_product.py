import pytest
from services.product_service import ProductService
from utils.logger import get_logger

# Get a logger instance
logger = get_logger(__name__)

@pytest.fixture(scope="module")
def product_service():
    """
    Fixture to initialize ProductService instance.
    """
    return ProductService()

def test_get_product(product_service):
    """
    Test getting product details by product ID.
    """
    product_id = 1
    response = product_service.get_product(product_id)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    logger.info(f"Product details: {response.json()}")

def test_create_product(product_service):
    """
    Test creating a new product.
    """
    product_data = {
        "name": "Laptop",
        "description": "A powerful laptop for developers",
        "price": 1500.00,
        "stock": 50
    }
    response = product_service.create_product(product_data)
    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    logger.info(f"Created product: {response.json()}")

def test_update_product(product_service):
    """
    Test updating an existing product's details.
    """
    product_id = 1
    updated_product_data = {
        "name": "Laptop Pro",
        "description": "An even more powerful laptop for developers",
        "price": 2000.00,
        "stock": 40
    }
    response = product_service.update_product(product_id, updated_product_data)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    logger.info(f"Updated product details: {response.json()}")

def test_delete_product(product_service):
    """
    Test deleting a product by product ID.
    """
    product_id = 1
    response = product_service.delete_product(product_id)
    assert response.status_code == 204, f"Expected 204 but got {response.status_code}"
    logger.info(f"Deleted product with ID: {product_id}")
