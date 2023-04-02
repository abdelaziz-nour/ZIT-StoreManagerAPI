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


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['post'])
def Register(request):
    try:
        user = CustomUser.objects.create_user(
            UserName=request.data["UserName"],
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
        UserName = request.data["UserName"]
        password = request.data["password"]
        user = authenticate(UserName=UserName, password=password)
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

authentication_classes(
    [TokenAuthentication, BaseAuthentication, SessionAuthentication])
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
            AddedProduct = Product(
                ProductName=request.data["ProductName"],
                ProductDecription=request.data["ProductDecription"],
                ProductPrice=request.data["ProductPrice"],
                Quantity=request.data["Quantity"],
                ProductImage=request.FILES["ProductImage"],
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
        logging.warning(f"Exception Name: {type('Token.DoesNotExist')}")
        logging.warning(f"Exception Desc: {'exception'}")
        return custom_response(message="Token Does Not Exist")
    except User.DoesNotExist:
        logging.warning(f"Exception Name: {type('User.DoesNotExist')}")
        logging.warning(f"Exception Desc: {'exception'}")
        return custom_response(message="User With Provided Token Does Not Exist")
