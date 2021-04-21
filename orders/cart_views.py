import json

from django.http.response import JsonResponse
from django.views         import View

from .models         import OrderProduct
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

            cart, created = user.order_set.get_or_create(
                status_id = 1,
                defaults  = {'total_price' : 0}
            )

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

                product, created = cart.orderproduct_set.get_or_create(
                    product_id    = product_id,
                    color_size_id = color_size_id,
                    bundle_id     = bundle_id,
                    defaults      = {'quantity' : quantity}
                )

                if not created:
                    product.quantity += quantity
                    product.save()

            cart.total_price += total_price
            cart.save()
            
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)

    @login_decorator
    def get(self, request):
        user = request.user

        cart, created = user.order_set.get_or_create(
            status_id = 1,
            defaults  = {'total_price' : 0}
        )

        cart_products = [
            {
                "product_id"       : product.product_id,
                "thumbnail_image"  : product.product.thumbnail_url,
                "name"             : product.product.name,
                "order_product_id" : product.id,
                "bundle_id"        : product.bundle_id if product.bundle else None,
                "bundle_name"      : product.bundle.name if product.bundle else None,
                "color_size_id"    : product.color_size_id if product.color_size else None,
                "color_name"       : product.color_size.color.name if product.color_size else None,
                "size_name"        : product.color_size.size.name if product.color_size else None,
                "default_price"    : product.product.price,
                "price_gap"        : product.bundle.price_gap if product.bundle else 0,
                "quantity"         : product.quantity
            } for product in cart.orderproduct_set.all()
        ]
        
        return JsonResponse({
            'cart_id'     : cart.id,
            'cart'        : cart_products, 
            'total_price' : cart.total_price
        }, status=200)

    @login_decorator
    def patch(self, request, item_id=None):
        try:
            user        = request.user
            data        = json.loads(request.body)
            quantity    = data['quantity']
            item_id     = item_id

            if not item_id:
                return JsonResponse({'MESSAGE' : 'INVALID PRODUCT'}, status=404)

            cart = user.order_set.filter(status__name='장바구니').first()

            if not cart:
                return JsonResponse({'MESSAGE' : 'INVALID CART'}, status=404)

            order_product = cart.orderproduct_set.filter(id=item_id).first()

            if not order_product:
                return JsonResponse({'MESSAGE' : 'INVALID ITEM'}, status=404)

            price = order_product.product.price

            if order_product.bundle:
                price += order_product.bundle.price_gap

            cart.total_price += (price * quantity)

            order_product.quantity += quantity
            
            order_product.save()
            cart.save()

            return JsonResponse({'MESSAGE' : 'SUCCCESS'}, status=204)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)

    @login_decorator
    def delete(self, request):
        try:
            user           = request.user
            delete_targets = request.GET.get('item_id')
            delete_targets = list(map(int, delete_targets.split(',')))

            cart = user.order_set.filter(status__name='장바구니').first()

            if not cart:
                return JsonResponse({'MESSAGE' : 'INVALID CART'}, status=404)

            targets = cart.orderproduct_set.filter(id__in=delete_targets)
            
            for target in targets:
                price = target.product.price

                if target.bundle:
                    price += target.bundle.price_gap

                cart.total_price -= price * (target.quantity)
            
            targets.delete()
            cart.save()

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=204)
            
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE ERROR'}, status=400)