from django.test import TestCase
from app.models import Product, Category
from app.factories import ProductFactory, CategoryFactory
class ProductReadTest(TestCase):
    def test_read_product_by_id(self):
        product = ProductFactory()

        fetched = Product.objects.get(id=product.id)

        self.assertEqual(fetched.name, product.name)
        self.assertEqual(fetched.price, product.price)
class ProductUpdateTest(TestCase):
    def test_update_product_price(self):
        product = ProductFactory(price=500)

        product.price = 750
        product.save()

        updated = Product.objects.get(id=product.id)
        self.assertEqual(updated.price, 750)
class ProductDeleteTest(TestCase):
    def test_delete_product(self):
        product = ProductFactory()
        product_id = product.id

        product.delete()

        self.assertFalse(Product.objects.filter(id=product_id).exists())
class ProductListTest(TestCase):
    def test_list_all_products(self):
        ProductFactory.create_batch(5)

        products = Product.objects.all()

        self.assertEqual(products.count(), 5)
class ProductFindByNameTest(TestCase):
    def test_find_product_by_name(self):
        ProductFactory(name="iPhone 15")
        ProductFactory(name="Samsung Galaxy")

        result = Product.objects.filter(name__icontains="iphone")

        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first().name, "iPhone 15")
class ProductFindByCategoryTest(TestCase):
    def test_find_products_by_category(self):
        electronics = CategoryFactory(name="Electronics")
        fashion = CategoryFactory(name="Fashion")

        ProductFactory(category=electronics)
        ProductFactory(category=electronics)
        ProductFactory(category=fashion)

        electronics_products = Product.objects.filter(category__name="Electronics")

        self.assertEqual(electronics_products.count(), 2)
class ProductFindByAvailabilityTest(TestCase):
    def test_find_available_products(self):
        ProductFactory(stock=10)   # available
        ProductFactory(stock=0)    # not available

        available_products = Product.objects.filter(is_available=True)

        self.assertEqual(available_products.count(), 1)
