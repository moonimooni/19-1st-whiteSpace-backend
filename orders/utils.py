from django.http.response import JsonResponse

from products.models import Product

def color_size_set(product_obj, color_id, size_id, bundle_id):
    if color_id and size_id:
        color_size = product_obj.colorsizeoption_set.filter(
            color_id = color_id, 
            size_id  = size_id
        ).first()

    if not (color_size) or \
    (bundle_id and not product_obj.bundleoption_set.filter(id=bundle_id).exists()):
        return

    return color_size