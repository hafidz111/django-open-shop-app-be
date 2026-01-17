from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    shop = models.CharField(max_length=100)
    price = models.PositiveIntegerField(help_text="Price in rupiah")
    sku = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=100)
    discount = models.PositiveIntegerField(default=0, help_text="Discount percentage")
    category = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    picture = models.URLField(blank=True)
    is_delete = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    @property
    def is_available(self):
        return self.stock > 0

    def soft_delete(self):
        if self.is_delete:
            raise ValueError("Product already deleted")
        self.is_delete = True
        self.save(update_fields=['is_delete'])