import datetime

from django.utils     import timezone
from django.db.models import When, Case

def annotate_is_new(queryset):
    return queryset.annotate(
        is_new = Case(
            When(
                created_at__gte = timezone.now() - datetime.timedelta(days=1),
                then = True
            ),
            default = False
        )
    )

def calculate_stock(product_obj):
    bundles_stock = sum(product_obj.bundleoption_set.values_list('stock', flat=True))
    color_sizes_stock = sum(product_obj.colorsizeoption_set.values_list('stock', flat=True))

    return bundles_stock + color_sizes_stock