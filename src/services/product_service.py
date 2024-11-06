from core.api_client import APIClient
from utils.logger import get_logger
from utils.config_loader import get_config_value

# Get a logger instance
logger = get_logger(__name__)


class ProductService:
    def __init__(self, api_client=None):
        self.api_client = api_client or APIClient(base_url=get_config_value("API_BASE_URL", "http://localhost:5000"))
        self.endpoint = "/products"

    def get_product(self, product_id):
        """
        Get a product's details by product ID.

        :param product_id: The ID of the product to retrieve
        :return: Response object
        """
        logger.info(f"Fetching product with ID: {product_id}")
        response = self.api_client.get(f"{self.endpoint}/{product_id}")
        return response

    def create_product(self, product_data):
        """
        Create a new product with the provided product data.

        :param product_data: Dictionary containing product data to create
        :return: Response object
        """
        logger.info(f"Creating a new product with data: {product_data}")
        response = self.api_client.post(self.endpoint, data=product_data)
        return response

    def update_product(self, product_id, product_data):
        """
        Update an existing product's details by product ID.

        :param product_id: The ID of the product to update
        :param product_data: Dictionary containing updated product data
        :return: Response object
        """
        logger.info(f"Updating product with ID: {product_id} with data: {product_data}")
        response = self.api_client.put(f"{self.endpoint}/{product_id}", data=product_data)
        return response

    def delete_product(self, product_id):
        """
        Delete a product by product ID.

        :param product_id: The ID of the product to delete
        :return: Response object
        """
        logger.info(f"Deleting product with ID: {product_id}")
        response = self.api_client.delete(f"{self.endpoint}/{product_id}")
        return response


# # Usage example
# if __name__ == "__main__":
#     product_service = ProductService()
#
#     # Example to get product details
#     response = product_service.get_product(product_id=1)
#     logger.info(f"Response: {response.status_code}, {response.json()}")
