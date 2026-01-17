from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from open_shop_app.serializers import ProductSerializer
from .models import Product


class ProductList(APIView):
    def post(self, request):
        products = ProductSerializer(data=request.data, context={'request': request})
        if products.is_valid(raise_exception=True):
            products.save()
            return Response(products.data, status=status.HTTP_201_CREATED)
        return Response(products.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        products = Product.objects.filter(is_delete=False)

        name = request.query_params.get('name')
        location = request.query_params.get('location')

        if name:
            products = products.filter(name__icontains=name)

        if location:
            products = products.filter(location__icontains=location)

        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )

        return Response(
            {"products": serializer.data},
            status=status.HTTP_200_OK
        )


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        try:
            product.soft_delete()
        except ValueError:
            return Response(
                {"detail": "Product already deleted"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
