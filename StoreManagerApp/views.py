import logging
from django.http import HttpResponse
from StoreManagerApp.helper import custom_response
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, BaseAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from datetime import datetime
import json


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['post'])
def Register(request):
    try:
        user = CustomUser.objects.create_user(
            username=request.data["username"],
            email=request.data["email"],
            PhoneNumber=request.data["PhoneNumber"],
            Gender=request.data["Gender"],
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
        return custom_response(message="something went wrong")


@api_view(['POST'])
def Login(request):
    try:
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
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


authentication_classes([TokenAuthentication, BaseAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def AddStore(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            AddedStore = Store(
                Owner=CurrentUser,
                Name=request.data["Name"],
                Image=request.FILES["Image"],
                CreatedBy=CurrentUser,
                CreatedOn=datetime.now()
            )
            AddedStore.save()
            return custom_response(message="Adding Store Successfully", success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Adding Failure")
    except Token.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="User With Provided Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")


authentication_classes([TokenAuthentication, BaseAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
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
    except Token.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="User With Provided Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

authentication_classes([TokenAuthentication, BaseAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def AddProduct(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        CurrentUser = User.objects.get(id=user.id)
        try:
            category = Category.objects.get(id=request.data.get('Category'))
            AddedProduct = Product(
                Name=request.data["Name"],
                Decription=request.data["Decription"],
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
    except Token.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="User With Provided Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")


authentication_classes([TokenAuthentication, BaseAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
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

            # Create the order and save it
            order = Orders(Customer=CurrentUser)
            order.CreatedBy = CurrentUser
            order.CreatedOn = datetime.now()
            order.save()

            for i, product_id in enumerate(products):
                product = Product.objects.get(pk=product_id)
                if product.Quantity - amounts[i] >= 0:
                    # If there is enough quantity, create a new OrderItem instance and add it to the order
                    product.Quantity -= amounts[i]
                    product.save()
                    ordereditem = OrderItem(Product=product, Quantity=amounts[i])
                    ordereditem.save()
                    order.OrderItems.add(ordereditem)
                else:
                    # If there is not enough quantity, return an error response
                    return custom_response(message="Insufficient Amount Of Product",
                                            data={
                                                "Product": product.Name,
                                                "AvailableAmount": product.Quantity,
                                                "OrederedAmount":amounts[i]
                                            })

            # Get the categories associated with the ordered products
            categories = Category.objects.filter(products__id__in=products)

            # Get the stores associated with the categories
            stores = categories.values_list('Store', flat=True).distinct()

            order.Stores.add(*stores)
            return custom_response(message="Adding Order Successfully", success=True)


        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Adding Failure")
    except Token.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="User With Provided Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")
    
authentication_classes([TokenAuthentication, BaseAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def GetStores(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try: 
            Stores=Store.objects.all()
            data = []
            for store in Stores:
                field = {
                    "id": store.pk,
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
    except Token.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="User With Provided Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")
    
authentication_classes([TokenAuthentication, BaseAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def GetProducts(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try: 
            Products=Product.objects.all()
            data = []
            for product in Products:
                field = {
                    "id": product.pk,
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
    except Token.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="User With Provided Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

authentication_classes([TokenAuthentication, BaseAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
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
                        "id": order.pk,
                        'Store': store.Name,
                        'CreatedBy': order.CreatedBy.username,
                        'CreatedOn': order.CreatedOn.strftime("%Y-%m-%d %H:%M:%S"),
                        'OrderItems': [],
                        
                    }
                    for order_item in order.OrderItems.all():
                        product = order_item.Product
                        if product.Category.Store == store:
                            item_data = {
                                'ProductName': product.Name,
                                'Price': product.Price,
                                'Quantity': order_item.Quantity,
                                'Subtotal': int(product.Price) * int(order_item.Quantity)
                            }
                            order_data['OrderItems'].append(item_data)
                            subtotal = int(product.Price) * int(order_item.Quantity)
                            total += subtotal
                    data.append(order_data)
            data.append({'Total':total})
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting Products Failure")
    except Token.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="User With Provided Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")

authentication_classes([TokenAuthentication, BaseAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def GetUsers(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try: 
            Users=User.objects.all()
            data = []
            for user in Users:
                store=Store.objects.get(Owner=user.id)
                field = {
                    "id": user.pk,
                    "UserName": user.username,
                    "Email": user.email,
                    "Store": store.Name,
                }
                data.append(field)
            print(data)
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting Users Failure")
    except Token.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="User With Provided Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")
    
authentication_classes([TokenAuthentication, BaseAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def GetStoreProducts(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try: 
            store = Store.objects.get(id=request.data["Store"])
            categories = Category.objects.filter(Store=store)
            products = Product.objects.filter(Category__in=categories)
            data = []
            for product in products:
                field = {
                    "id": product.pk,
                    "Name": product.Name,
                    "Category": product.Category.Name,
                    "Price": product.Price,
                }
                data.append(field)
            print(data)
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting Products Failure")
    except Token.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="User With Provided Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")
    
authentication_classes([TokenAuthentication, BaseAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def GetStoreOrders(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try:
            store = Store.objects.get(id=request.data["Store"])
            orders = Orders.objects.filter(Stores=store)
            data = []
            total = 0
            for order in orders:
                order_data = {
                    "id": order.pk,
                    'CreatedBy': order.CreatedBy.username,
                    'CreatedOn': order.CreatedOn.strftime("%Y-%m-%d %H:%M:%S"),
                    'OrderItems': [],
                    
                }
                for order_item in order.OrderItems.all():
                    product = order_item.Product
                    if product.Category.Store == store:
                        item_data = {
                            'ProductName': product.Name,
                            'Price': product.Price,
                            'Quantity': order_item.Quantity,
                            'Subtotal': int(product.Price) * int(order_item.Quantity)
                        }
                        order_data['OrderItems'].append(item_data)
                        subtotal = int(product.Price) * int(order_item.Quantity)
                        total += subtotal
                data.append(order_data)
            data.append({'Total':total})
            return custom_response(data=data, success=True)

        except BaseException as exception:
            logging.warning(f"Exception Name: {type(exception).__name__}")
            logging.warning(f"Exception Desc: {exception}")
            return custom_response(message="Getting Store Orders Failure")
    except Token.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="User With Provided Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")
    
authentication_classes([TokenAuthentication, BaseAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def GetStoreCategories(request):
    User = get_user_model()
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        token_obj = Token.objects.get(key=token)
        user = User.objects.get(id=token_obj.user_id)
        User.objects.get(id=user.id)
        try: 
            store = Store.objects.get(id=request.data["Store"])
            categories = Category.objects.filter(Store=store)
            data = []
            for category in categories:
                field = {
                    "id": category.pk,
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
    except Token.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="User With Provided Token Does Not Exist")
    except IndexError as exception:
        logging.warning(f"Exception Name: {type(exception).__name__}")
        logging.warning(f"Exception Desc: {exception}")
        return custom_response(message="No Token Provided")