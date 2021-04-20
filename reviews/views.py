import json

from django.http.response import JsonResponse
from django.views import View

from users.utils     import login_decorator
from products.models import Product
from .models         import Review, ReviewImage

class ReviewView(View):
    @login_decorator
    def post(self, request, product_id=None):
        try:
            user          = request.user
            data          = json.loads(request.body)
            product_id    = product_id
            color_size_id = data.get('color_size_id', None)
            bundle_id     = data.get('bundle_id', None)
            text          = data['text']
            rating        = data['rating']
            image_urls    = data['image_urls']

            if not product_id or not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'MESSAGE' : 'INVALID PRODUCT'}, status=404)

            product = Product.objects.get(id=product_id)

            if  (color_size_id and 
                not product.colorsizeoption_set.filter(id=color_size_id).exists()) or \
                (bundle_id and not product.bundleoption_set.filter(id=bundle_id).exists()):
                    return JsonResponse({'MESSAGE' : 'INVALID OPTION'}, status=404)

            review = Review.objects.create(
                author        = user,
                product_id    = product_id,
                color_size_id = color_size_id,
                bundle_id     = bundle_id,
                text          = text,
                rating        = rating
            )

            review_images = [
                ReviewImage(
                    review = review,
                    image_url = image_url
                ) for image_url in image_urls
            ]

            ReviewImage.objects.bulk_create(review_images)

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)

    def get(self, request, product_id=None):
        if not product_id or not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'MESSAGE' : 'INVALID PRODUCT'}, status=404)
        
        product = Product.objects.get(id=product_id)

        reviews = list(
            {
                'product_name'  : review.product.name,
                'thumbnail_url' : review.product.thumbnail_url,
                'author'        : review.author.name,
                'text'          : review.text,
                'rating'        : review.rating,
                'bundle'        : review.bundle.name if review.bundle else None,
                'color'         : review.color_size.color.name if review.color_size else None,
                'size'          : review.color_size.size.name if review.color_size else None,
                'image_urls'    : [image.image_url for image in review.reviewimage_set.all()]
            } for review in product.review_set.all()
        )

        count   = product.review_set.count()
        ratings = [product.review_set.filter(rating=i+1).count() for i in range(5)]

        return JsonResponse({
            'count'   : count, 
            'reviews' : reviews, 
            'one'     : ratings[0], 
            'two'     : ratings[1], 
            'three'   : ratings[2], 
            'four'    : ratings[3], 
            'five'    : ratings[4]}, status=200)