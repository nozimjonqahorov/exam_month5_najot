from django.urls import path
from .views import TransactionMainView, CategoryCreatePostView

urlpatterns = [
    path('', TransactionMainView.as_view(), name='transaction_main'),
    path('category/add/', CategoryCreatePostView.as_view(), name='category_add_post'),
]