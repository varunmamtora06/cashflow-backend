from .models import Category

def category_exists(user, category_name):
    try:
        Category.objects.get(by_user=user, category_name=category_name)
        return True
    except Category.DoesNotExist:
        return False