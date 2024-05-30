from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    def __self__ (self):
       return self.name
       
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    exist = models.BooleanField(default=False,null=True,blank=False)
    stock = models.PositiveIntegerField(default=0)
    image=models.ImageField(default=False,null=True,blank=True)
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''    
        return url
        
class Order(models.Model) :
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id =models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.id)
    def get_cart_total(self):
       orderitems=self.order_items.all()
       total=sum([item.get_total for item in orderitems if item.product.exist or item.product.stock>0])
       return total
    def get_cart_items(self):
       orderitems=self.order_items.all()
       total=sum([item.quantity for item in orderitems if item.product.exist or item.product.stock>0])
       return total
    @property
    def shipping(self):
        shipping=False
        orderitems=self.order_items.all()
        for i in orderitems:
            if i.product.exist==False and i.product.stock>0:
                shipping=True
        return shipping

      
class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True,null=True) 
    Order=models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True,null=True,related_name='order_items')
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total= self.product.price * self.quantity
        return total
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address=models.CharField(max_length=200, null=True) 
    city = models.CharField(max_length=200, null=True)
    state=models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added=models.DateTimeField(auto_now_add=False)
    def __str__(self):
        return self.address