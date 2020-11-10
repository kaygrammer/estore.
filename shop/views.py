from django.shortcuts import render,get_object_or_404, HttpResponseRedirect
from .models import Product,Category
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from . models import Product
from django.db.models import Q
from .forms import Searchform


def index(request,  category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    paginator = Paginator(products, 6)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'category': category,
               'categories': categories,
               'products': products,
              'page': page}
    return render(request, 'shop/product/index.html', context)


def search(request):
    form = Searchform()
    query = None
    results = []
    if 'query' in request.GET:
        form = Searchform(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.annotate(
                search = SearchVector('name', 'category'),
            ).filter(search=query)
    return render(request, 'shop/product/search.html', {'form':form,
                                                        'query':query,
                                                        'results':results})



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category=category)
    paginator = Paginator(products, 6)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'category': category,
               'categories': categories,
               'products': products,
               'page' : page}
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})


