import pytest
import responses
import json
from pathlib import Path
from jsonschema import validate, ValidationError
from src.services.product_service import ProductService
from src.utils.logger import get_logger
from typing import Generator

# Get a logger instance
logger = get_logger(__name__)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

schema_path = ROOT_DIR / "schemas" / "product_schema.json"

with open(schema_path, "r") as f:
    PRODUCT_SCHEMA = json.load(f)


@pytest.fixture(scope="module")
def product_service() -> Generator[ProductService, None, None]:
    """
    Fixture to initialize ProductService instance.

    :return: Initialized ProductService instance
    """
    logger.info("Initializing ProductService instance")
    yield ProductService()


@responses.activate
def test_get_product(product_service: ProductService) -> None:
    """
    Test getting product details by product ID.

    :param product_service: Initialized ProductService instance
    """
    product_id: int = 1
    url = f"http://localhost:5000/products/{product_id}"

    # Mocking the GET request
    responses.add(
        responses.GET,
        url,
        json={
            "id": product_id,
            "name": "Laptop",
            "description": "A powerful laptop for developers",
            "price": 1500.00,
            "stock": 50,
        },
        status=200,
    )

    logger.info(f"Testing GET product with ID: {product_id}")
    response = product_service.get_product(product_id)
    logger.debug(f"Response received: {response.status_code}, {response.json()}")

    # Validate response schema
    try:
        validate(instance=response.json(), schema=PRODUCT_SCHEMA)
        logger.info(
            f"GET product response schema validation passed for product ID: {product_id}"
        )
    except ValidationError as e:
        logger.error(f"GET product response schema validation failed: {e}")
        pytest.fail(f"Schema validation failed: {e}")

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    logger.info(f"GET product test passed for product ID: {product_id}")


@responses.activate
def test_create_product(product_service: ProductService) -> None:
    """
    Test creating a new product.

    :param product_service: Initialized ProductService instance
    """
    product_data: dict = {
        "name": "Laptop",
        "description": "A powerful laptop for developers",
        "price": 1500.00,
        "stock": 50,
    }
    url = "http://localhost:5000/products"

    # Mocking the POST request
    responses.add(responses.POST, url, json={"id": 1, **product_data}, status=201)

    logger.info("Testing CREATE product")
    logger.debug(f"Product data being sent: {product_data}")
    response = product_service.create_product(product_data)
    logger.debug(f"Response received: {response.status_code}, {response.json()}")

    # Validate response schema
    try:
        validate(instance=response.json(), schema=PRODUCT_SCHEMA)
        logger.info("CREATE product response schema validation passed")
    except ValidationError as e:
        logger.error(f"CREATE product response schema validation failed: {e}")
        pytest.fail(f"Schema validation failed: {e}")

    assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    logger.info("CREATE product test passed")


@responses.activate
def test_update_product(product_service: ProductService) -> None:
    """
    Test updating an existing product's details.

    :param product_service: Initialized ProductService instance
    """
    product_id: int = 1
    updated_product_data: dict = {
        "name": "Laptop Pro",
        "description": "An even more powerful laptop for developers",
        "price": 2000.00,
        "stock": 40,
    }
    url = f"http://localhost:5000/products/{product_id}"

    # Mocking the PUT request
    responses.add(
        responses.PUT, url, json={"id": product_id, **updated_product_data}, status=200
    )

    logger.info(f"Testing UPDATE product with ID: {product_id}")
    logger.debug(f"Updated product data being sent: {updated_product_data}")
    response = product_service.update_product(product_id, updated_product_data)
    logger.debug(f"Response received: {response.status_code}, {response.json()}")

    # Validate response schema
    try:
        validate(instance=response.json(), schema=PRODUCT_SCHEMA)
        logger.info(
            f"UPDATE product response schema validation passed for product ID: {product_id}"
        )
    except ValidationError as e:
        logger.error(f"UPDATE product response schema validation failed: {e}")
        pytest.fail(f"Schema validation failed: {e}")

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    logger.info(f"UPDATE product test passed for product ID: {product_id}")


@responses.activate
def test_delete_product(product_service: ProductService) -> None:
    """
    Test deleting a product by product ID.

    :param product_service: Initialized ProductService instance
    """
    product_id: int = 1
    url = f"http://localhost:5000/products/{product_id}"

    # Mocking the DELETE request
    responses.add(responses.DELETE, url, status=204)

    logger.info(f"Testing DELETE product with ID: {product_id}")
    response = product_service.delete_product(product_id)
    logger.debug(f"Response received: {response.status_code}")

    assert response.status_code == 204, f"Expected 204 but got {response.status_code}"
    logger.info(f"DELETE product test passed for product ID: {product_id}")
