from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Category, Product
from django.shortcuts import get_object_or_404

# Create your views here.


class IndexView(TemplateView):
    template_name = 'shop/index.html'

class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category/category_list.html'
    context_object_name = 'categories'

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        queryset = Product.objects.select_related('category').filter(available=True)
        print(queryset)
        print(category_slug)

        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            print(self.category)
            queryset = queryset.filter(category=self.category)
            print(queryset)
        else:
            self.category = None

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['categories'] = Category.objects.all()
        context['category'] = self.category
        #context['category'] = getattr(self, 'category', None)
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        category_slug = self.kwargs.get('category_slug')
        product_slug = self.kwargs.get('slug')
        
        category = get_object_or_404(Category, slug=category_slug)
        product = get_object_or_404(Product, category=category, slug=product_slug, available=True)
        return product
    
class ContactView(TemplateView):
    template_name = 'shop/contact.html'