from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    PhoneNumber = models.CharField(max_length=20,blank=False,null=False)
    Gender = models.CharField(choices=[('Male', 'Male'),
    ('Female', 'Female'),],max_length=10,blank=False,null=False)
    IsStoreManager= models.BooleanField(default=False)
    IsAdmin= models.BooleanField(default=False)
    IsSimpleUser= models.BooleanField(default=False)
    IsAdvertiser= models.BooleanField(default=False)
    def __str__(self):
        return self.username

class BaseFields(models.Model):
    CreatedBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  related_name="%(class)s_created_by", null=False, blank=False,)
    CreatedOn = models.DateTimeField(null=False, blank=False)
    UpdatedBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  related_name="%(class)s_updated_by", null=True, blank=True)
    UpdatedOn = models.DateTimeField(null=True, blank=True)
    DeletedBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  related_name="%(class)s_deleted_by", null=True, blank=True)
    DeletedOn = models.DateTimeField(null=True, blank=True)
    IsDeleted = models.BooleanField(default=False, blank=False, null=False)
    class Meta:
        abstract = True


class Store(BaseFields):
    Owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50, blank=False, null=False)
    Image = models.ImageField(upload_to='Stores/', height_field=None, width_field=None, max_length=None)
    def __str__(self):
        return self.Name


class Category(BaseFields):
    Store = models.ForeignKey(Store, on_delete=models.CASCADE, blank=False, null=False, related_name='categories')
    Name = models.CharField(max_length=50, blank=False, null=False)
    Image = models.ImageField(upload_to='Categories/', height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return self.Name


class Product(BaseFields):
    Name = models.CharField(max_length=50, blank=False, null=False)
    Decription = models.TextField(max_length=255, blank=False, null=False)
    Price = models.CharField(max_length=50, blank=False, null=False)
    Quantity = models.IntegerField(blank=False, null=False)
    Image = models.ImageField(upload_to='Images/', height_field=None, width_field=None, max_length=None)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, related_name='products')
    def __str__(self):
        return self.Name
    
class OrderItem(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.IntegerField(blank=False, null=False, default=1)
    def __str__(self):
        return self.Product.Name


class Orders(BaseFields):
    Customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    Stores = models.ManyToManyField(Store)
    OrderItems = models.ManyToManyField(OrderItem)
    Location = models.TextField(max_length=255, blank=False, null=False)
    Status = models.CharField(choices=[('Preparing', 'Preparing'),
    ('OnDelivery', 'OnDelivery'),('Delivered', 'Delivered'),('Canceled', 'Canceled'),],max_length=10,blank=False,null=False,default='Preparing')
    def __str__(self):
        return self.Customer.username

