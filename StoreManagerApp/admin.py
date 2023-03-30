from django.contrib import admin
from .models import *


admin.site.register(CustomUser)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Orders)
class ArticleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
