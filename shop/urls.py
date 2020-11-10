from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.search, name='search'),
    path('list/', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

]