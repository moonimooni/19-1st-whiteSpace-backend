import json
import datetime

from django.db.models     import Count, Q
from django.http.response import JsonResponse
from django.views         import View

from users.utils     import login_decorator
from products.models import Product
from .models         import Review, ReviewImage
from .utils          import count_ratings, average_rating
from my_settings     import S3_CLIENT, AWS_STORAGE_BUCKET_NAME

class ReviewView(View):
    @login_decorator
    def post(self, request, product_id=None):
        try:
            s3_client = S3_CLIENT
            user      = request.user
            data      = request.POST

            product_id    = product_id
            color_size_id = data.get('color_size_id', None)
            bundle_id     = data.get('bundle_id', None)
            text          = data['text']
            rating        = data['rating']
            images        = request.FILES.getlist('images', [])

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

            for image in images:
                now = str(datetime.datetime.now()).replace(' ', '')[:-7]

                s3_client.upload_fileobj(
                    image,
                    AWS_STORAGE_BUCKET_NAME,
                    f'{now}.{image.name}',
                    ExtraArgs = {
                        "ContentType" : image.content_type
                    }
                )

            review.reviewimage_set.bulk_create([
                ReviewImage(
                    image_url = f"http://{AWS_STORAGE_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{now}.{image.name}",
                    review    = review
                )
                for image in images
            ])

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)

    def get(self, request, product_id=None):
        if not product_id or not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'MESSAGE' : 'INVALID PRODUCT'}, status=404)
        
        product_qs = Product.objects.filter(id=product_id)
        product_qs = product_qs.annotate(
            one   = count_ratings(1),
            two   = count_ratings(2),
            three = count_ratings(3),
            four  = count_ratings(4),
            five  = count_ratings(5)
        )

        product = product_qs.first()

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

        count = product.review_set.count()

        return JsonResponse({
            'average_rating' : average_rating(
                product.one,
                product.two,
                product.three,
                product.four,
                product.five
            ),
            'count'   : count, 
            'reviews' : reviews, 
            'one'     : product.one, 
            'two'     : product.two, 
            'three'   : product.three, 
            'four'    : product.four, 
            'five'    : product.five}, status=200)

class ReviewAuthView(View):
    @login_decorator
    def get(self, request, product_id=None):
        if not product_id or not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'MESSAGE' : 'INVALID PRODUCT'}, status=404)

        user        = request.user
        user_orders = user.order_set.filter(status__name='배송완료')

        if user_orders.filter(product__id=product_id).exists():
            return JsonResponse({'MESSAGE' : 'OK'}, status=200)
            
        return JsonResponse({'MESSAGE' : 'DENIED'}, status=401)