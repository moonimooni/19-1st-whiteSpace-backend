from django.views         import View
from django.http.response import JsonResponse
from django.db.models     import Sum

from .models     import Category, Product, BannerImage
from .utils      import annotate_is_new, calculate_stock
from my_settings import PAGING_LIMIT

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

        products_stock = [calculate_stock(product) for product in best_sellers_qs]

        best_sellers = [
            {
                'id' : product.id,
                'name' : product.name,
                'price' : product.price,
                'thumbnail_url' : product.thumbnail_url,
                'stock' : stock,
                'is_limited' : stock <= 20,
                'is_new' : product.is_new,
            } for product, stock in zip(best_sellers_qs, products_stock)
        ]

        return JsonResponse({'banner_images' : banner_images, 'best_sellers' : best_sellers}, status=200)

class ProductsView(View):
    def get(self, request):
        try: 
            category_id = int(request.GET.get('category', 0))
            page        = int(request.GET.get('page', 0))

            if not page:
                return JsonResponse({'MESSAGE' : 'INVALID PAGINATION'}, status=400)

            if category_id and not Category.objects.filter(id=category_id).exists():
                return JsonResponse({'MESSAGE' : 'INVALID CATEGORY'}, status=404)

            if not category_id:
                products_qs   = Product.objects.all()
                category_name = 'ALL'
            else:
                products_qs   = Product.objects.filter(category_id=category_id)
                category_name = Category.objects.get(id=category_id).name
            
            products_count = products_qs.count()

            offset = (page - 1) * PAGING_LIMIT
            limit  = offset + PAGING_LIMIT
            
            products_qs    = annotate_is_new(products_qs).order_by('-created_at')[offset:limit]
            products_stock = [calculate_stock(product) for product in products_qs]

            products = [
                {
                    'id'            : product.id,
                    'name'          : product.name,
                    'price'         : product.price,
                    'thumbnail_url' : product.thumbnail_url,
                    'stock'         : stock,
                    'is_limited'    : stock <= 20,
                    'is_new'        : product.is_new,
                } for product, stock in zip(products_qs, products_stock)
            ]
            
            return JsonResponse({
                'count'    : products_count, 
                'category' : category_name,
                'products' : products
            }, status=200)

        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE ERROR'}, status=400)