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