import datetime

from django.utils         import timezone
from django.views         import View
from django.http.response import JsonResponse
from django.db.models     import When, Case, Sum

from .models import Category, Product, BannerImage

class NavView(View):
    def get(self, request):
        categories = [
            {
                "category_id" : category.id,
                "category_name" : category.name
            } for category in Category.objects.all()
        ]

        return JsonResponse({'categories' : categories}, status=200)

class MainView(View):
    def get(self, request):
        
        banner_images = [banner.image_url for banner in BannerImage.objects.all()]

        best_sellers_qs = Product.objects.annotate(sales_record = Sum('orderproduct__quantity'))
        best_sellers_qs = best_sellers_qs.order_by('-sales_record')[:3]

        best_sellers_qs = Product.objects \
            .annotate(
                is_new = Case(
                    When(
                        created_at__gte = timezone.now() - datetime.timedelta(days=1), 
                        then=True
                    ),
                    default = False
                )
            )
            
        best_sellers = []
        for product in best_sellers_qs:
            bundles_stock     = sum(product.bundleoption_set.values_list('stock', flat=True))
            color_sizes_stock = sum(product.colorsizeoption_set.values_list('stock', flat=True))

            product_info = {
                'id' : product.id,
                'name' : product.name,
                'price' : product.price,
                'thumbnail_url' : product.thumbnail_url,
                'stock' : bundles_stock + color_sizes_stock,
                'is_new' : product.is_new
            }
            best_sellers.append(product_info)
        
        return JsonResponse({'banner_images' : banner_images, 'best_sellers' : best_sellers}, status=200)