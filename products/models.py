from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45, unique=True)
    
    class Meta:
        db_table = 'categories'

class Product(models.Model):
    name          = models.CharField(max_length=45, unique=True)
    price         = models.DecimalField(max_digits=8, decimal_places=2)
    description   = models.CharField(max_length=255)
    discount_rate = models.DecimalField(max_digits=3, decimal_places=2)
    thumbnail_url = models.URLField(max_length=5000)
    size          = models.ManyToManyField('Size', through='ColorSizeOption')
    color         = models.ManyToManyField('Color', through='ColorSizeOption')
    category      = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'

class SubImage(models.Model):
    image_url = models.URLField(max_length=5000)
    color     = models.ForeignKey('Color', on_delete=models.CASCADE, null=True, blank=True)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'sub_images'

class DescriptionImage(models.Model):
    image_url = models.URLField(max_length=5000)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    sequence  = models.SmallIntegerField()

    class Meta:
        db_table = 'desription_images'

class Color(models.Model):
    name     = models.CharField(max_length=45)
    hex_code = models.CharField(max_length=45, unique=True)
    
    class Meta:
        db_table = 'colors'

class Size(models.Model):
    name = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'names'

class BundleOption(models.Model):
    name      = models.CharField(max_length=45, unique=True)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_gap = models.DecimalField(max_digits=8, decimal_places=2)
    stock     = models.IntegerField()
    
    class Meta:
        db_table = 'bundle_options'

class ColorSizeOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color   = models.ForeignKey(Color, on_delete=models.CASCADE)
    size    = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock   = models.IntegerField()
    
    class Meta:
        db_table = 'color_size_options'

class BannerImage(models.Model):
    image_url = models.URLField(max_length=5000)
    
    class Meta:
        db_table = 'banner_images'
