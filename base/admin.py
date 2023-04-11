from django.contrib import admin
from .models import Product
from .models import Category
from mptt.admin import DraggableMPTTAdmin

class CategoryAdmin(DraggableMPTTAdmin):
    pass

admin.site.register(Category, CategoryAdmin )

admin.site.register(Product)