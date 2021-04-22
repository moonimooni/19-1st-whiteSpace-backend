import json

from django.http.response import JsonResponse
from django.views         import View

from .models         import Order
from users.utils     import login_decorator

class OrderFromCartView(View):
    @login_decorator
    def post(self, request):
        try:
            user           = request.user
            data           = json.loads(request.body)

            cart_id        = data['cart_id']
            total_price    = data['total_price']
            postal_code    = data['postal_code']
            main_address   = data['main_address']
            detail_address = data['detail_address']
            phone_number   = data['phone_number']
            
            selected_products = request.GET.get('item_id', None)

            cart = Order.objects.get(id=cart_id)

            if selected_products:
                selected_products = list(map(int, selected_products.split(',')))
                ordering_items    = cart.orderproduct_set.filter(id__in=selected_products)

                new_order = Order.objects.create(
                    user = user,
                    status_id = 5,
                    total_price = 0
                )
                ordering_items.update(order=new_order)

                cart.total_price -= total_price
                cart.save()

            else:
                cart.status_id = 5
                new_order      = cart

            address, created = user.address_set.get_or_create(
                postal_code    = postal_code, 
                main_address   = main_address, 
                detail_address = detail_address,
                phone_number   = phone_number,
                defaults       = {'is_main' : True}
            )

            new_order.address     = address
            new_order.total_price = total_price
            
            new_order.save()

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)