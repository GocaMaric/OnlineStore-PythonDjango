from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"Category: {self.name}"

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='items/', blank=True)
    is_sold = models.BooleanField(default=False, db_index=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Item: {self.name} by {self.created_by.username}"

    class Meta:
        ordering = ('-created_at',)
