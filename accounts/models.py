from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(upload_to='images/', default='profile1.png')
    date_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name or ''


class Tag(models.Model):
    tag = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.tag


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )

    # The first element in each tuple is the value
    # The second element is the human readable text

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=20, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_added = models.DateField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    date_created = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)
    note = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.product.name


# 1 customer can place many orders customer->order 1->n
# 1 product can be placed in multiple orders
# eg. 1 Book and n people can order that book(n copies)
# Thus, product -> order => 1 -> n
