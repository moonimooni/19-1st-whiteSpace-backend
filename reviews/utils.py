from django.db.models import Count, Q

def count_ratings(rating):
    return Count('review__rating', filter=Q(review__rating=rating))