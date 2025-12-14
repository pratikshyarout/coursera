from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from app.models import Product
from app.serializers import ProductSerializer
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = Product.objects.all()

        name = self.request.query_params.get("name")
        category = self.request.query_params.get("category")
        available = self.request.query_params.get("available")

        if name:
            queryset = queryset.filter(name__icontains=name)

        if category:
            queryset = queryset.filter(category__name__iexact=category)

        if available is not None:
            if available.lower() == "true":
                queryset = queryset.filter(is_available=True)
            elif available.lower() == "false":
                queryset = queryset.filter(is_available=False)

        return queryset
