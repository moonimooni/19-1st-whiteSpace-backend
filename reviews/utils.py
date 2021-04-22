from django.db.models import Count, Q

def count_ratings(rating):
    return Count('review__rating', filter=Q(review__rating=rating))

def average_rating(one,two,three,four,five):
    ratings = [one, two, three, four, five]

    divider       = sum(ratings)
    total_ratings = sum(list(map(lambda x : x[1] * (x[0]+1), enumerate(ratings))))

    return round(total_ratings / divider, 1)