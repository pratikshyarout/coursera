from behave import given
from app.factories import ProductFactory, CategoryFactory


@given("the database is populated with BDD test data")
def step_load_bdd_data(context):
    # Create categories
    electronics = CategoryFactory(name="Electronics")
    fashion = CategoryFactory(name="Fashion")

    # Create products
    ProductFactory(
        name="iPhone 15",
        category=electronics,
        stock=10
    )

    ProductFactory(
        name="MacBook Air",
        category=electronics,
        stock=0
    )

    ProductFactory(
        name="T-Shirt",
        category=fashion,
        stock=25
    )

    context.data_loaded = True
