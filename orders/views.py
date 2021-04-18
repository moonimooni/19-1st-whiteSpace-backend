import json

from django.http.response import JsonResponse
from django.views         import View
from django.db.models     import Q

from .models         import Order, Status, OrderProduct
from users.utils     import login_decorator
from products.models import Product

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            user        = request.user
            data        = json.loads(request.body)
            products    = data['products']
            total_price = data['total_price']

            cart = user.order_set.filter(status__name='장바구니').first()
            
            if not cart:
                cart_status = Status.objects.get(name='장바구니')
                cart = Order(
                    user        = user,
                    status      = cart_status,
                    total_price = 0
                )
                cart.save()

            newly_added_products = []
            existing_products    = []

            for product in products:
                product_id    = product['product_id']
                bundle_id     = product.get('bundle_id', None)
                color_size_id = product.get('color_size_id', None)
                quantity      = product['quantity']

                if not Product.objects.filter(id=product_id).exists():
                    return JsonResponse({'MESSAGE' : 'INVALID PRODUCT'}, status=404)

                product = Product.objects.get(id=product_id)

                if (bundle_id and not product.bundleoption_set.filter(id=bundle_id).exists()) or \
                    (color_size_id and not product.colorsizeoption_set.filter(id=color_size_id).exists()):
                        return JsonResponse({'MESSAGE' : 'INVALID OPTION'}, status=404)

                existing_product = cart.orderproduct_set.filter(
                    Q(product_id    = product_id) & 
                    Q(color_size_id = color_size_id) & 
                    Q(bundle_id     = bundle_id)).first()

                if existing_product:
                    existing_product.quantity += quantity
                    existing_products.append(existing_product)
                else:
                    newly_added_products.append(
                        OrderProduct(
                            order         = cart,
                            product_id    = product_id,
                            color_size_id = color_size_id,
                            bundle_id     = bundle_id,
                            quantity      = quantity
                        )
                    )

            OrderProduct.objects.bulk_update(existing_products, ['quantity'])
            OrderProduct.objects.bulk_create(newly_added_products)
            
            cart.total_price += total_price
            cart.save()

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)