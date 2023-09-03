from django.contrib import admin
import models

# Register your models here.
admin.register(models.Shop)
admin.register(models.Category)
admin.register(models.Product)
admin.register(models.ProductInfo)
admin.register(models.ProductParameter)
admin.register(models.Order)
admin.register(models.OrderItem)