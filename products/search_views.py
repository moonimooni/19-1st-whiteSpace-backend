from django.views         import View
from django.db.models     import Q
from django.http.response import JsonResponse

from .models import Product
from .utils  import annotate_is_new, calculate_stock, return_products_list

class SearchView(View):
    def get(self, request):
        keyword = request.GET.get('keyword', None)

        if not keyword:
            return JsonResponse({'MESSAGE' : 'NO KEYWORD'})

        if keyword:
            products_qs = Product.objects.filter(
                Q(name__icontains        = keyword) |
                Q(description__icontains = keyword)
            )
        
        if not products_qs:
            return JsonResponse({'MESSAGE' : 'NO MATCH'}, status=404)

        products_qs    = annotate_is_new(products_qs).order_by('-created_at')
        products_stock = [calculate_stock(product) for product in products_qs]
        
        products = return_products_list(products_qs, products_stock)

        return JsonResponse({'products' : products}, status=200)