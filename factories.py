# factories.py

import factory
from faker import Faker
from decimal import Decimal
from random import randint, choice
from django.utils.text import slugify

from app.models import Product, Category   # adjust app name if needed

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyFunction(lambda: fake.word().capitalize())
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))

    description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=3))

    price = factory.LazyFunction(
        lambda: Decimal(randint(199, 9999))  # ₹199 – ₹9999
    )

    discount_price = factory.LazyAttribute(
        lambda obj: obj.price - Decimal(randint(0, int(obj.price * Decimal("0.3"))))
        if choice([True, False]) else None
    )

    stock = factory.LazyFunction(lambda: randint(0, 200))
    is_available = factory.LazyAttribute(lambda obj: obj.stock > 0)

    category = factory.SubFactory(CategoryFactory)

    sku = factory.LazyFunction(
        lambda: fake.unique.bothify(text="SKU-####-???")
    )

    rating = factory.LazyFunction(
        lambda: round(fake.pyfloat(min_value=2.5, max_value=5.0), 1)
    )

    created_at = factory.LazyFunction(fake.date_time_this_year)
    updated_at = factory.LazyFunction(fake.date_time_this_year)
