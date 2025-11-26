from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()  # store Cloudinary URL

    def __str__(self):
        return self.name
    
