from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),

    # authentication
    path('register', views.Register),#zit
    path('login', views.Login),#zit
    path('adminlogin', views.AdminLogin),#web
    path('storemanagerlogin', views.StoreManagerLogin),#sma

    path('addstore', views.AddStore),#web
    path('addcategory', views.AddCategory),#sma
    path('addproduct', views.AddProduct),#sma
    path('addorder', views.AddOrder),#zit

    path('getusers', views.GetUsers),#web
    path('getstores', views.GetStores),#web-zit##########
    path('getproducts', views.GetProducts),#web
    path('getorders', views.GetOrders),#web

    path('getstorecategories', views.GetStoreCategories),#zit-sma-web
    path('getcategoryproducts', views.GetCategoryProducts),#zit-sma-web
    path('getstoreproducts', views.GetStoreProducts),#web
    path('getstoreorders', views.GetStoreOrders),#sma-web
    path('getuserorders', views.GetUserOrders),#sma-web

    path('deletestore', views.DeleteStore),#web
    path('deletecategory', views.DeleteCategory),#web-sma
    path('deleteproduct', views.DeleteProduct),#sma

    path('addproductquantity', views.AddProductQuantity),#sma
    path('changeorderstatus', views.ChangeOrderStatus),#sma
    path('changeaccountpermissions', views.ChangeAccountPermissions),#web

    path('changepassword', views.ChangePassword),#sma
    path('updateproduct', views.UpdateProduct),#sma
    path('updatestore', views.UpdateStore),#web
    path('updatecategory', views.UpdateCategory),#sma

    ]