from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


from base.models import Product
from base.models import Category

from base.serializers import ProductSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@api_view(['GET'])
def getProducts(request):
   
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    products = Product.objects.order_by('-createdt')
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    productsList = paginator.get_page(page)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page })

@api_view(['GET'])
def getProductsHomeCarousel(request):
     products = Product.objects.order_by('-price')[0:5]
     serializer = ProductSerializer(products, many=True)
     return Response({'products': serializer.data})


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getUserProducts(request):
     user = request.user
     products = Product.objects.filter(user=user)
     serializer = ProductSerializer(products, many=True)
     return Response({'products': serializer.data})


@api_view(['POST'])
def createProduct(request):
    user = request.user

    product = Product.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        
        condition='',
        location = '',
        descripption=''
    )

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def updateProduct(request,pk):
    data = request.data
    product = Product.objects.get(_id=pk)
    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.condition = data['condition']
    product.location = data['location']
    product.descripption = data['description']
    product.phoneNumber = data['phoneNumber']
    product.category = data['category']
    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Product Deleted')