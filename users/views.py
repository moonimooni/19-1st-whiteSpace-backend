

class Product(models.Model):
    name            = models.CharField(max_length=50, unique=True)
    price           = models.DecimalField(max_digits=8, decimal_places=2)
    discount_rate   = models.DecimalField(max_digits=3, decimal_places=2)
    thumbnail_url   = models.URLField(max_length=500)
    category        = models.ForeignKey('Category', on_delete=models.CASCADE)
    description     = models.CharField(max_length=300)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    color = models.ManyToManyField('Color', through='ColorSizeOption')
    size = models.ManyToManyField('Size', through='ColorSizeOption')

    class Meta:
        db_table = 'products'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'categories'


class BundleOption(models.Model):
    name    = models.CharField(max_length=50, unique=True) 
    price   = models.DecimalField(max_digits=8, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock   = models.IntegerField()
    
    class Meta:
        db_table = 'bundle_options'

class DescriptionImage(models.Model):
    image_url = models.URLField(max_length = 500) 
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    sequence  = models.SmallIntegerField()
    
    class Meta:
        db_table = 'description_images'

class SubImage(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.URLField(max_length = 500)
    color     = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        db_table = 'sub_images'

class Color(models.Model):
    hex_code = models.CharField(max_length=45)
    name     = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'colors'

class Size(models.Model):
    name = models.CharField(max_length=45 unique=True)

    class Meta:
        db_table = 'sizes'

class ColorSizeOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color   = models.ForeignKey(Color, on_delete=models.CASCADE)
    size    = models.ForeignKey(size, on_delete=models.CASCADE)
    stock   = models.IntegerField()

    class Meta:
        db_table = 'color_size_options'

class BannerImage(models.Model):
    image_url = models.URLField(max_length=500)
    class Meta:
        db_table = 'banner_images'


