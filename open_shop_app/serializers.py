from rest_framework import serializers
from rest_framework.reverse import reverse

from open_shop_app.models import Product

class ProductSerializer(serializers.ModelSerializer):
    is_available = serializers.ReadOnlyField()
    is_delete = serializers.ReadOnlyField()
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'shop', 'price', 'sku','description', 'location', 'discount', 'category', 'stock','is_available', 'picture', 'is_delete', 'updatedAt', 'createdAt', '_links']


    def get__links(self, obj):
        request = self.context.get('request')
        return [
            {
                "rel": "self",
                "href": reverse('product-list', request=request),
                "action": "POST",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": reverse('product-detail', kwargs={'pk': obj.pk}, request=request),
                "action": "GET",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": reverse('product-detail', kwargs={'pk': obj.pk}, request=request),
                "action": "PUT",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": reverse('product-detail', kwargs={'pk': obj.pk}, request=request),
                "action": "DELETE",
                "types": ["application/json"]
            }
        ]