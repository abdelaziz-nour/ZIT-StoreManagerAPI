from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),

    # authentication
    path('register', views.Register),
    path('login', views.Login),
    path('adminlogin', views.AdminLogin),

    path('addstore', views.AddStore),
    path('addcategory', views.AddCategory),
    path('addproduct', views.AddProduct),
    path('addorder', views.AddOrder),

    path('getusers', views.GetUsers),
    path('getstores', views.GetStores),
    path('getproducts', views.GetProducts),
    path('getorders', views.GetOrders),

    path('getstorecategories', views.GetStoreCategories),
    path('getcategoryproducts', views.GetCategoryProducts),
    path('getstoreproducts', views.GetStoreProducts),
    path('getstoreorders', views.GetStoreOrders),

    path('deletestore', views.DeleteStore),
    path('deletecategory', views.DeleteCategory),
    path('deleteproduct', views.DeleteProduct),

    path('addproductquantity', views.AddProductQuantity),
    ]