from django.urls import path
from base.views import product_views as views


urlpatterns = [
    path('', views.getProducts, name="products"),
    path('price/', views.getProductsByPrice, name="price-products"),
    path('user/', views.getUserProducts, name="user-products"),
    path('create/', views.createProduct, name="product-create"),
    path('upload/', views.uploadImage, name="image-upload"),
    path('upload2/', views.uploadImage2, name="image2-upload"),
    path('upload3/', views.uploadImage3, name="image3-upload"),
    path('upload4/', views.uploadImage4, name="image4-upload"),
    path('<str:pk>/', views.getProduct, name="product"),
    path('delete/<str:pk>/', views.deleteProduct, name="product-delete"),
    path('update/<str:pk>/', views.updateProduct, name="product-update"),
]
