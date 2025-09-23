from .models import Review
from django.shortcuts import get_object_or_404

def get_reviews_for_product(product_id):
    return Review.objects.filter(product_id=product_id)

def create_review(user, data):
    return Review.objects.create(user=user, **data)

def update_review(review, data):
    for field, value in data.items():
        setattr(review, field, value)
    review.save()
    return review

def delete_review(review):
    review.delete()

def get_review_by_id(pk):
    return get_object_or_404(Review, pk=pk)
