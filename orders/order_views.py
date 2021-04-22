import json

from django.db            import transaction
from django.http.response import JsonResponse
from django.views         import View

from .models         import Order
from users.utils     import login_decorator

class OrderFromCartView(View):
    @login_decorator
    @transaction.atomic
    def post(self, request):
        try:
            user           = request.user
            data           = json.loads(request.body)

            postal_code    = data['postal_code']
            main_address   = data['main_address']
            detail_address = data['detail_address']
            phone_number   = data['phone_number']

            cart_id        = data['cart_id']
            cart_items     = data['cart_items']
            total_price    = data['total_price']

            address, created = user.address_set.get_or_create(
                postal_code    = postal_code, 
                main_address   = main_address, 
                detail_address = detail_address,
                phone_number   = phone_number,
                defaults       = {'is_main' : True}
            )

            new_order = Order.objects.create(
                user = user,
                status_id = 5,
                total_price = 0
            )

            cart = Order.objects.get(id=cart_id)

            if cart.user != user:
                return JsonResponse({'MESSAGE' : 'UNAUTHORIZED ACCESS'}, status=401)

            ordering_items    = cart.orderproduct_set.filter(id__in=cart_items)
            new_order.address = address
            
            cart.total_price      -= total_price
            new_order.total_price += total_price
            
            ordering_items.update(order_id=new_order.id)
            cart.save()
            new_order.save()

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)