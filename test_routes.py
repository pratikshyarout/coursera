from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from app.models import Product
from app.factories import ProductFactory, CategoryFactory
class TestListAllProducts(APITestCase):
    def test_list_all_products(self):
        ProductFactory.create_batch(5)

        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
class TestReadProduct(APITestCase):
    def test_read_product_by_id(self):
        product = ProductFactory()

        response = self.client.get(f"/api/products/{product.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], product.name)
class TestUpdateProduct(APITestCase):
    def test_update_product_price(self):
        product = ProductFactory(price=500)

        payload = {
            "price": 750
        }

        response = self.client.patch(
            f"/api/products/{product.id}/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.price, 750)
class TestDeleteProduct(APITestCase):
    def test_delete_product(self):
        product = ProductFactory()

        response = self.client.delete(f"/api/products/{product.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=product.id).exists())
class TestListByName(APITestCase):
    def test_list_products_by_name(self):
        ProductFactory(name="iPhone 15")
        ProductFactory(name="Samsung Galaxy")

        response = self.client.get("/api/products/?name=iphone")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "iPhone 15")
class TestListByCategory(APITestCase):
    def test_list_products_by_category(self):
        electronics = CategoryFactory(name="Electronics")
        fashion = CategoryFactory(name="Fashion")

        ProductFactory(category=electronics)
        ProductFactory(category=electronics)
        ProductFactory(category=fashion)

        response = self.client.get("/api/products/?category=Electronics")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
class TestListByAvailability(APITestCase):
    def test_list_available_products(self):
        ProductFactory(stock=10)  # available
        ProductFactory(stock=0)   # unavailable

        response = self.client.get("/api/products/?available=true")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]["is_available"])
