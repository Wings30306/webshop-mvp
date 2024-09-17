from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class ShopItem(models.Model):
    item_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    featured_image = CloudinaryField('image')

    def __str__(self):
        return self.item_name