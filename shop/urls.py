from django.urls import path
from .views import ProductListView, ProductDetailView, ContactView, CategoryListView, IndexView

app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('catalog/', CategoryListView.as_view(), name='category_list'),
    path('catalog/category/<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('catalog/category/<slug:category_slug>/product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]