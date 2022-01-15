from .models import Category

def category_exists(user, category_name):
    try:
        category = Category.objects.get(by_user=user, category_name=category_name)
        return True, category
    except Category.DoesNotExist:
        return False, None