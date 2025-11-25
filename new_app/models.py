from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=225)  # hashed password
    auth_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.email
