from django.db import models

class Order(models.Model):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product     = models.ManyToManyField('products.Product', through='OrderProduct')
    status      = models.ForeignKey('Status', on_delete=models.CASCADE)
    address     = models.ForeignKey('users.Address', on_delete=models.CASCADE)
    used_coupon = models.ForeignKey('users.Coupon', on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'

class OrderProduct(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE)
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    color_size = models.ForeignKey('products.ColorSizeOption', on_delete=models.CASCADE, null=True, blank=True)
    bundle     = models.ForeignKey('products.BundleOption', on_delete=models.CASCADE, null=True, blank=True)
    quantity   = models.IntegerField()
    
    class Meta:
        db_table = 'order_products'

class Status(models.Model):
    name = models.CharField(max_length=45, unique=True)
    
    class Meta:
        db_table = 'status'
