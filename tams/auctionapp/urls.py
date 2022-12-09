from django.urls import path

from . import views, api
from auctionapp.views import profile_api

app_name = 'auctionapp'
urlpatterns = [
    path('', views.loginUser, name='login'),
    path('signup', views.signup, name='signup'),
    path('api/profile/<int:user_id>/', profile_api, name="profile api"),
    path('api/products/', views.fetch_products, name='fetch_products'),
    path('api/products/<int:product_id>/', views.fetch_products_id, name='fetch_product_id'),
    path('items/<int:product_id>', views.product_details, name='product_details')
    ## path('api/search/', api.api_search, name='api_search'),
]