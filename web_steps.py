import json
from behave import when, then
from django.test import Client
from app.models import Product
def before_scenario(context, scenario):
    context.client = Client()
    context.response = None
@when('I send a GET request to "{url}"')
def step_get_request(context, url):
    context.response = context.client.get(url)
@when('I send a PATCH request to "{url}" with payload:')
def step_patch_request(context, url):
    payload = json.loads(context.text)
    context.response = context.client.patch(
        url,
        data=json.dumps(payload),
        content_type="application/json"
    )
@when('I send a DELETE request to "{url}"')
def step_delete_request(context, url):
    context.response = context.client.delete(url)
@then('the response status code should be {status:d}')
def step_check_status_code(context, status):
    assert context.response.status_code == status
@then('the response should contain a list of products')
def step_check_list(context):
    data = json.loads(context.response.content)
    assert isinstance(data, list)
    assert len(data) > 0
@then('the response should contain product details')
def step_check_product_details(context):
    data = json.loads(context.response.content)
    assert "name" in data
    assert "price" in data
@then('the product price should be updated to {price:d}')
def step_check_price_updated(context, price):
    product = Product.objects.first()
    assert product.price == price
@then('the product should no longer exist')
def step_check_product_deleted(context):
    assert Product.objects.count() == 0
@then('the response should contain products with name containing "{name}"')
def step_check_name_search(context, name):
    data = json.loads(context.response.content)
    for product in data:
        assert name.lower() in product["name"].lower()
@then('the response should contain only products from category "{category}"')
def step_check_category_search(context, category):
    data = json.loads(context.response.content)
    for product in data:
        assert product["category"]["name"] == category
@then('the response should contain only available products')
def step_check_availability(context):
    data = json.loads(context.response.content)
    for product in data:
        assert product["is_available"] is True
