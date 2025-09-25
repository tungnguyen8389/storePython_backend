from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from categories.models import Category

class CategoryService:
    @staticmethod
    def get_category_by_id(category_id):
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise NotFound("Category not found")

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def create_category(data):
        if Category.objects.filter(name=data.get('name')).exists():
            raise ValidationError("Category with this name already exists")
        category = Category.objects.create(**data)
        return category

    @staticmethod
    def update_category(category_id, data):
        category = CategoryService.get_category_by_id(category_id)
        if 'name' in data and Category.objects.filter(name=data['name']).exclude(id=category_id).exists():
            raise ValidationError("Category with this name already exists")
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    @staticmethod
    def delete_category(category_id):
        category = CategoryService.get_category_by_id(category_id)
        category.delete()