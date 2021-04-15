from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=100, unique=True)
    password     = models.CharField(max_length=200)
    name         = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=45, unique=True)
    is_active    = models.BooleanField(default=True)
    mileage      = models.PositiveIntegerField(default=0)
    coupon       = models.ManyToManyField('Coupon', through='UserCoupon')
    wish         = models.ManyToManyField('products.Product', through='WishList')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Address(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    postal_code    = models.CharField(max_length=45)
    main_address   = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=100)
    is_main        = models.BooleanField()
    phone_number   = models.CharField(max_length=45)

    class Meta:
        db_table = 'addresses'

class WishList(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    is_deleted = models.BooleanField()

    class Meta:
        db_table = 'wish_lists'

class Coupon(models.Model):
    name           = models.CharField(max_length=100)
    discount_rate  = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    valid_days     = models.SmallIntegerField()

    class Meta:
        db_table = 'coupons'

class UserCoupon(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon    = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    is_used   = models.SmallIntegerField()
    expire_at = models.DateTimeField()

    class Meta:
        db_table = 'users_coupons'
