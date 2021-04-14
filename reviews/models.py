from django.db import models

class Review(models.Model):
    author  = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='author')
    product = models.ForeignKey('orders.OrderProduct', on_delete=models.CASCADE)
    text    = models.TextField()
    rating  = models.SmallIntegerField()
    like    = models.ManyToManyField('users.User', through='ReviewLike')
    
    class Meta:
        db_table = 'reviews'

class ReviewImage(models.Model):
    review    = models.ForeignKey(Review, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500)
    
    class Meta:
        db_table = 'review_images'

class Comment(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'comments'

class ReviewLike(models.Model):
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'review_likes'
