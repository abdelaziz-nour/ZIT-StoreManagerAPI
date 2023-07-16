import logging
from operator import itemgetter
from django.http import HttpResponse
from StoreManagerApp.helper import custom_response
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import json
from django.db.models import Count,OuterRef,Subquery


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@api_view(['post'])
def Register(request):
    try:
        if 'IsStoreManager' in request.data:
            user = CustomUser.objects.create_user(
                username=request.data["username"],
                email=request.data["email"],
                PhoneNumber=request.data["PhoneNumber"],
                Gender=request.data["Gender"],
                IsStoreManager=True,
                password=request.data["password"],
            )
            if user:
                token = Token.objects.create(user=user)
                return custom_response(
                    data={
                        'token': token.key,
                    },
                    success=True,
                )
            else:
                return custom_response(message="User account not created")

        elif 'IsAdvertiser' in request.data:
            user = CustomUser.objects.create_user(
                username=request.data["username"],
                email=request.data["email"],
                PhoneNumber=request.data["PhoneNumber"],
                Gender=request.data["Gender"],
                IsAdvertiser=True,
                password=request.data["password"],
            )
            if user:
                token = Token.objects.create(user=user)
                return custom_response(
                    data={
                        'token': token.key,
                    },
                    success=True,
                )
            else:
                return custom_response(message="User account not created")

        elif 'IsAdmin' in request.data:
            user = CustomUser.objects.create_user(
                username=request.data["username"],
                email=request.data["email"],
                PhoneNumber=request.data["PhoneNumber"],
                Gender=request.data["Gender"],
                IsAdmin=True,
                password=request.data["password"],
            )
            if user:
                token = Token.objects.create(user=user)
                return custom_response(
                    data={
                        'token': token.key,
                    },
                    success=True,
                )
            else:
                return custom_response(message="User account not created")

        else:
            user = CustomUser.objects.create_user(
                username=request.data["username"],
                email=request.data["email"],
                PhoneNumber=request.data["PhoneNumber"],
                Gender=request.data["Gender"],
                IsSimpleUser=True,
                password=request.data["password"],
            )
            if user:
                token = Token.objects.create(user=user)
                return custom_response(
                    data={
                        'token': token.key,
                    },
                    success=True,
                )
            else:
                return custom_response(message="User account not created")

    except BaseException as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Something went wrong")

@api_view(['POST'])
def Login(request):
    try:
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None and user.IsSimpleUser or user.is_staff:
            token = Token.objects.get(user_id=user)

            return custom_response(
                data={'token': token.key},
                success=True
            )
        else:
            return custom_response(message="User Not Found")
    except BaseException as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Authentication Failure")

@api_view(['POST'])
def AdminLogin(request):
    try:
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff or user.IsAdmin:
            token = Token.objects.get(user_id=user)

            return custom_response(
                data={'token': token.key},
                success=True
            )
        else:
            return custom_response(message="User Not Found")
    except BaseException as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Authentication Failure")

@api_view(['POST'])
def StoreManagerLogin(request):
    try:
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff or user.IsStoreManager:
            try :
                store =Store.objects.get(Owner=user.id)
            except BaseException as exception:
                return custom_response(message="User Does Not Have A Store")
            token = Token.objects.get(user_id=user)
            return custom_response(
                data={'token': token.key,
                    'StoreName':store.Name,
                    'StoreID':store.StoreID,
                    'StoreImage':store.Image.url,
                    },
                success=True
            )
            
        else:
            return custom_response(message="No Store Manager Account Match Giving Credentials")

    except BaseException as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Authentication Failure")

@api_view(['POST'])
def AddStore(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        AddedStore = Store(
            Owner=User.objects.get(email=request.data["Email"]),
            Name=request.data["Name"],
            Image=request.FILES["Image"],
            CreatedBy=CurrentUser,
            CreatedOn=datetime.now()
        )
        AddedStore.save()
        return custom_response(message="Adding Store Successfully", success=True)
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def AddCategory(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        store = Store.objects.get(Owner=CurrentUser)
        try:
            AddedCategory = Category(
                Store=store,
                Name=request.data["Name"],
                Image=request.FILES["Image"],
                CreatedBy=CurrentUser,
                CreatedOn=datetime.now()
            )
            AddedCategory.save()
            return custom_response(message="Adding Category Successfully", success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Adding Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def AddProduct(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            category = Category.objects.get(CategoryID=request.data.get('Category'))
            AddedProduct = Product(
                Name=request.data["Name"],
                Description=request.data["Description"],
                Price=request.data["Price"],
                Quantity=request.data["Quantity"],
                Category=category,
                Image=request.FILES["Image"],
                CreatedBy=CurrentUser,
                CreatedOn=datetime.now()
            )
            AddedProduct.save()
            return custom_response(message="Adding Product Successfully", success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Adding Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def AddOrder(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            data = json.loads(request.body)
            products = data.get('OrderedProducts')
            amounts = data.get('Amounts')
            location = data.get('Location')

            # Create the order and save it
            order = Orders(Customer=CurrentUser)
            order.Location = location
            order.CreatedBy = CurrentUser
            order.CreatedOn = datetime.now()
            

            for i, product_id in enumerate(products):
                product = Product.objects.get(ProductID=product_id)
                if product.Quantity - amounts[i] >= 0:
                    # If there is enough quantity, create a new OrderItem instance and add it to the order
                    product.Quantity -= amounts[i]
                    product.save()
                    ordereditem = OrderItem(
                        Product=product, Quantity=amounts[i])
                    ordereditem.save()
                    order.save()
                    order.OrderItems.add(ordereditem)
                else:
                    # If there is not enough quantity, return an error response
                    return custom_response(message="Insufficient Amount Of Product",
                                           data={
                                               "Product": product.Name,
                                               "AvailableAmount": product.Quantity,
                                               "OrderedAmount": amounts[i]
                                           })

            # Get the categories associated with the ordered products
            categories = Category.objects.filter(products__ProductID__in=products)

            # Get the stores associated with the categories
            stores = categories.values_list('Store', flat=True).distinct()

            order.Stores.add(*stores)
            return custom_response(message="Adding Order Successfully", success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Adding Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['GET'])
def GetStores(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try:
            Stores = Store.objects.filter(IsDeleted=False)
            data = []
            for store in Stores:
                field = {
                    "id": store.StoreID,
                    "Owner": store.Owner.username,
                    "Name": store.Name,
                    "Image": store.Image.url,
                }
                data.append(field)
            print(data)
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting Stores Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['GET'])
def GetProducts(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try:
            Products = Product.objects.filter(IsDeleted=False)
            data = []
            for product in Products:
                field = {
                    "id": product.ProductID,
                    "Store": product.Category.Store.Name,
                    "Name": product.Name,
                    "Image": product.Image.url,
                }
                data.append(field)
            print(data)
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting Products Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['GET'])
def GetOrders(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try:
            orders = Orders.objects.all()
            data = []
            total = 0
            for order in orders:
                for store in order.Stores.all():
                    order_data = {
                        "id": order.OrderID,
                        'Store': store.Name,
                        'Status': order.Status,
                        'Location': order.Location,
                        'CreatedBy': order.CreatedBy.username,
                        'CreatedOn': order.CreatedOn.strftime("%Y-%m-%d %H:%M:%S"),
                        'OrderItems': [],

                    }
                    for order_item in order.OrderItems.all():
                        product = order_item.Product
                        if product.Category.Store == store:
                            item_data = {
                                "id": product.ProductID,
                                'ProductName': product.Name,
                                'Price': product.Price,
                                'Quantity': order_item.Quantity,
                                'Subtotal': int(product.Price) * int(order_item.Quantity)
                            }
                            order_data['OrderItems'].append(item_data)
                            subtotal = int(product.Price) * \
                                int(order_item.Quantity)
                            total += subtotal
                    data.append(order_data)
            data.append({'Total': total})
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting Products Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['GET'])
def GetUsers(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try:
            users = User.objects.all()
            data = []
            for user in users:
                store = Store.objects.filter(Owner=user.id).first()
                print('Store :>'+str(store))
                field = {
                    "id": user.pk,
                    "UserName": user.username,
                    "Email": user.email,
                    "Store": store.Name if store else "None",
                    "StoreDeletion": store.IsDeleted if store else False,
                }
                data.append(field)
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting Users Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def GetStoreProducts(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try:
            store = Store.objects.get(StoreID=request.data["Store"])
            categories = Category.objects.filter(Store=store, IsDeleted=False)
            products = Product.objects.filter(
                Category__in=categories, IsDeleted=False)
            data = []
            for product in products:
                field = {
                    "id": product.ProductID,
                    "Name": product.Name,
                    "Description": product.Description,
                    "Category": product.Category.Name,
                    "Price": product.Price,
                    "Image": product.Image.url,
                }
                data.append(field)
            print(data)
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting Products Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def GetStoreOrders(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try:
            store = Store.objects.get(StoreID=request.data["Store"])
            orders = Orders.objects.filter(Stores=store)
            data = []
            total = 0
            for order in orders:
                order_data = {
                    "id": order.OrderID,
                    "Status": order.Status,
                    "Location": order.Location,
                    'CreatedBy': order.CreatedBy.username,
                    'CreatedOn': order.CreatedOn.strftime("%Y-%m-%d %H:%M:%S"),
                    'OrderItems': [],

                }
                for order_item in order.OrderItems.all():
                    product = order_item.Product
                    if product.Category.Store == store:
                        item_data = {
                            "id": product.ProductID,
                            'ProductName': product.Name,
                            'Price': product.Price,
                            'Quantity': order_item.Quantity,
                            'Subtotal': int(product.Price) * int(order_item.Quantity)
                        }
                        order_data['OrderItems'].append(item_data)
                        subtotal = int(product.Price) * \
                            int(order_item.Quantity)
                        total += subtotal
                data.append(order_data)
            data.append({'Total': total})
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting Store Orders Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def GetStoreCategories(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try:
            store = Store.objects.get(StoreID=request.data["Store"])
            categories = Category.objects.filter(Store=store, IsDeleted=False)
            data = []
            for category in categories:
                field = {
                    "id": category.CategoryID,
                    "Name": category.Name,
                    "Image": category.Image.url,
                }
                data.append(field)
            print(data)
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting Store Categories Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def GetCategoryProducts(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try:
            category = Category.objects.get(CategoryID=request.data['Category'])
            products = Product.objects.filter(
                Category=category, IsDeleted=False)
            data = []
            for product in products:
                product_data = {
                    "id": product.ProductID,
                    "Name": product.Name,
                    "Price": product.Price,
                    "Description": product.Description,
                    "Quantity": product.Quantity,
                    "Image": product.Image.url
                }
                data.append(product_data)
            print(data)
            return custom_response(data=data, success=True)

        except Category.DoesNotExist:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Category with provided ID does not exist")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token does not exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No token provided")

@api_view(['Get'])
def GetUserOrders(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        currentUser = User.objects.get(id=user.id)
        try:
            orders = Orders.objects.filter(Customer=currentUser)
            data = []
            total = 0
            for order in orders:
                order_data = {
                    "id": order.OrderID,
                    "Status": order.Status,
                    "Location": order.Location,
                    'CreatedBy': order.CreatedBy.username,
                    'CreatedOn': order.CreatedOn.strftime("%Y-%m-%d %H:%M:%S"),
                    'OrderItems': [],

                }
                for order_item in order.OrderItems.all():
                    product = order_item.Product
                    item_data = {
                        "id": product.ProductID,
                        'ProductName': product.Name,
                        'Price': product.Price,
                        'Quantity': order_item.Quantity,
                        'Image': product.Image.url,
                        'Subtotal': int(product.Price) * int(order_item.Quantity)
                    }
                    order_data['OrderItems'].append(item_data)
                    subtotal = int(product.Price) * \
                        int(order_item.Quantity)
                    total += subtotal
                data.append(order_data)
            data.append({'Total': total})
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting User Orders Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def DeleteStore(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            store = Store.objects.get(StoreID=request.data["Store"])
            store.IsDeleted = True
            store.DeletedBy = CurrentUser
            store.DeletedOn = datetime.now()
            store.save()
            return custom_response(message='Store Deleted Successfully', success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Deleting Store Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def DeleteCategory(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            category = Category.objects.get(CategoryID=request.data["Category"])
            category.IsDeleted = True
            category.DeletedBy = CurrentUser
            category.DeletedOn = datetime.now()
            category.save()
            return custom_response(message='Store Category Successfully', success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Deleting Category Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def DeleteProduct(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            product = Product.objects.get(ProductID=request.data["Product"])
            product.IsDeleted = True
            product.DeletedBy = CurrentUser
            product.DeletedOn = datetime.now()
            product.save()
            return custom_response(message='Store Product Successfully', success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Deleting Product Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def AddProductQuantity(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            product = Product.objects.get(ProductID=request.data["Product"])
            product.Quantity = request.data["Quantity"]
            product.UpdatedBy = CurrentUser
            product.UpdatedOn = datetime.now()
            product.save()
            return custom_response(message='Product Add Quantity Successfully', success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Adding Product Quantity Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def ChangeOrderStatus(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            order = Orders.objects.get(OrderID=request.data["Order"])
            print(request.data["Status"])
            if request.data["Status"] == 'OnDelivery':
                order.Status = 'OnDelivery'
                order.UpdatedBy = CurrentUser
                order.UpdatedOn = datetime.now()
                order.save()
                return custom_response(message='Order Status Changed Successfully', success=True)
            elif request.data["Status"] == 'Delivered':
                order.Status = 'Delivered'
                order.UpdatedBy = CurrentUser
                order.UpdatedOn = datetime.now()
                order.save()
                return custom_response(message='Order Status Changed Successfully', success=True)
            elif request.data["Status"] == 'Canceled':
                order.Status = 'Canceled'
                order.UpdatedBy = CurrentUser
                order.UpdatedOn = datetime.now()
                order.save()
                return custom_response(message='Order Status Changed Successfully', success=True)
            else:
                return custom_response(message="Invalid Order Status")
        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Changing Order Status Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def ChangeAccountPermissions(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            UpdatedUser=User.objects.get(email=request.data["Email"]),
            UpdatedUser[0].IsStoreManager=request.data["IsStoreManager"]
            UpdatedUser[0].IsAdmin=request.data["IsAdmin"]
            UpdatedUser[0].IsSimpleUser=request.data["IsSimpleUser"]
            UpdatedUser[0].IsAdvertiser=request.data["IsAdvertiser"]
            UpdatedUser[0].UpdatedBy = CurrentUser
            UpdatedUser[0].UpdatedOn = datetime.now()
            UpdatedUser[0].save()
            return custom_response(message="Changing Account Permissions Success",success=True)
        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Changing Account Permissions Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def ChangePassword(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            current_password = request.data['Password']
            new_password = request.data['NewPassword']
            confirm_password = request.data['ConfirmPassword']
            # Check if the entered current password matches the user's actual password
            if CurrentUser.check_password(current_password):
                # Validate the new password and confirm password
                if new_password == confirm_password:
                    # Set the new password
                    CurrentUser.set_password(new_password)
                    CurrentUser.save()
                    return custom_response(message="Changing Password Success",success=True)
                else:
                    return custom_response(message='New password and confirm password do not match.')
            else:
                return custom_response(message='Incorrect current password.')
        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Changing Account Password Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def UpdateProduct(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            product = Product.objects.get(ProductID=request.data["Product"])
            fields = ['Name', 'Description', 'Price', 'Quantity','Image']
            for field in fields:
                if field in request.data:
                    setattr(product, field, request.data[field])
            product.UpdatedBy = CurrentUser
            product.UpdatedOn = datetime.now()
            product.save()
            return custom_response(message= 'Product updated successfully.',success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Product updated Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['POST'])
def UpdateStore(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            store = Store.objects.get(StoreID=request.data["Store"])
            fields = ['Name','Image']
            for field in fields:
                if field in request.data:
                    setattr(store, field, request.data[field])
            store.UpdatedBy = CurrentUser
            store.UpdatedOn = datetime.now()
            store.save()
            return custom_response(message= 'Store updated successfully.',success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Store Update Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")
    
@api_view(['POST'])
def UpdateCategory(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            category = Category.objects.get(CategoryID=request.data["Category"])
            fields = ['Name','Image']
            for field in fields:
                if field in request.data:
                    setattr(category, field, request.data[field])
            category.UpdatedBy = CurrentUser
            category.UpdatedOn = datetime.now()
            category.save()
            return custom_response(message= 'Category updated successfully.',success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Category updated Failure")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['GET'])
def GetMostOrderedStores(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try:
            thirty_days_ago = datetime.today() - timedelta(days=30)
            stores = Store.objects.filter(IsDeleted=False)

            stores_with_orders = []
            for store in stores:
                num_orders = Orders.objects.filter(Stores=store, CreatedOn__gte=thirty_days_ago).count()
                stores_with_orders.append((store, num_orders))
            #sorting stores_with_orders according to the index 1 (not 0) which is num_orders
            stores_with_orders.sort(key=itemgetter(1), reverse=True)

            data = []
            for store, num_orders in stores_with_orders:
                field = {
                    "id": store.StoreID,
                    "Owner": store.Owner.username,
                    "Name": store.Name,
                    "Image": store.Image.url,
                    "OrdersCount": num_orders
                }
                data.append(field)


            return custom_response(data=data, success=True)

        except Exception as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Failed to retrieve stores with most orders")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

@api_view(['GET'])
def GetMostOrderedProducts(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try:
            thirty_days_ago = datetime.now() - timedelta(days=30)
            products = Product.objects.filter(IsDeleted=False)
            products_with_orders = []
            for product in products:
                num_orders = Orders.objects.filter(OrderItems__Product=product, CreatedOn__gte=thirty_days_ago).count()
                products_with_orders.append((product, num_orders))
            #sorting stores_with_orders according to the index 1 (not 0) which is num_orders
            products_with_orders.sort(key=itemgetter(1), reverse=True)

            data = []
            for product, num_orders in products_with_orders:
                field = {
                    "id": product.ProductID,
                    "Name": product.Name,
                    "Description": product.Description,
                    "Price": product.Price,
                    "Quantity": product.Quantity,
                    "Image": product.Image.url,
                    "OrdersCount": num_orders
                }
                data.append(field)

            return custom_response(data=data, success=True)

        except Exception as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Failed to retrieve most ordered products")
    except Token.DoesNotExist as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")