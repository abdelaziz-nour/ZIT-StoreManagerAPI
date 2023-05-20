from django.contrib import admin
from .models import *

class StoreAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Owner', 'StoreID', )
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Store', 'CategoryID', )
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Name', 'ProductID')
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('Customer',"Status", 'OrderID' )

admin.site.register(CustomUser)
admin.site.register(Store,StoreAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Orders,OrdersAdmin)

