from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


Genders = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

class CustomUser(AbstractUser):
    PhoneNumber = models.CharField(max_length=20,blank=False,null=False)
    Gender = models.CharField(choices=Genders,max_length=10,blank=False,null=False)

class BaseFields(models.Model):
    CreatedBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=False, blank=False,)
    CreatedOn = models.DateTimeField(null=False, blank=False)
    UpdatedBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="%(class)s_updated_by", null=True, blank=True)
    UpdatedOn = models.DateTimeField(null=True, blank=True)
    DeletedBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="%(class)s_deleted_by", null=True, blank=True)
    DeletedOn = models.DateTimeField(null=True, blank=True)
    IsDeleted = models.BooleanField(default=False,blank=False,null=False)
    class Meta:
        abstract = True

class Store(BaseFields):
    Owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE,blank=False,null=False)
    StoreName = models.CharField(max_length=50, blank=False, null=False)
    Categories = models.ManyToManyField('Category',blank=True,null=True)
    def __str__(self):
        return self.StoreName

class Category(BaseFields):
    Store = models.ForeignKey(Store, on_delete=models.CASCADE,blank=False,null=False)
    CategoryName = models.CharField(max_length=50,blank=False,null=False)
    Products = models.ManyToManyField('Product',blank=True,null=True)
    def __str__(self):
        return self.CategoryName
    

class Product(BaseFields):
    ProductName=models.CharField(max_length=50,blank=False,null=False)
    ProductDecription=models.CharField(max_length=50,blank=False,null=False)
    ProductPrice=models.CharField(max_length=50,blank=False,null=False )
    ProductImage=models.ImageField(upload_to='Images/', height_field=None, width_field=None, max_length=None)############################################################

    def __str__(self):
        return self.ProductName

class Orders(BaseFields):
    Customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=False,null=False)
    Stores = models.ManyToManyField(Store,blank=False,null=False)
    OrderedProducts = models.ManyToManyField('Product',blank=False,null=False)
    def __str__(self):
        return self.Customer.username







