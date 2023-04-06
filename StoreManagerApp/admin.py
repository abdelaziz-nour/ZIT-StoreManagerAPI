from django.contrib import admin
from .models import *


admin.site.register(CustomUser)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Orders)

