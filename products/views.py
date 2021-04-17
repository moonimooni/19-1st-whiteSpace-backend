from django.views         import View
from django.http.response import JsonResponse
from django.db.models     import Sum

from .models import Category, Product, BannerImage
from .utils  import annotate_is_new, calculate_stock

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

        best_sellers_qs = annotate_is_new(
            Product.objects
                .annotate(sales_record = Sum('orderproduct__quantity'))
                .order_by('-sales_record')[:3]
        )

        best_sellers = []

        for product in best_sellers_qs:
            stock      = calculate_stock(product)
            is_limited = stock <= 20
            
            best_sellers.append(
                {
                    'id' : product.id,
                    'name' : product.name,
                    'price' : product.price,
                    'thumbnail_url' : product.thumbnail_url,
                    'stock' : stock,
                    'is_limited' : is_limited,
                    'is_new' : product.is_new,
                }
            )

        return JsonResponse({'banner_images' : banner_images, 'best_sellers' : best_sellers}, status=200)