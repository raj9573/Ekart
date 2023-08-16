from django.contrib import admin

# Register your models here.
from app.models import *

admin.site.register(Product)

admin.site.register(UserProfile)

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Review)

admin.site.register(Category)

admin.site.register(Cart)