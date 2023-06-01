from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

from base.models import Product, Category, Favorite
from django.contrib.auth.models import User

from base.serializers import ProductSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from base.tasks import product_updated

@api_view(['GET'])
def getProducts(request):
   
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    products = Product.objects.filter(name__icontains=query).order_by('-createdt')
    paginator = Paginator(products, 4)
    page = request.query_params.get('page')
    try:
        productsList = paginator.page(page)
    except PageNotAnInteger:
        productsList = paginator.page(1)
    except EmptyPage:
        productsList = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    
    serializer = ProductSerializer(productsList, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages':paginator.num_pages })

@api_view(['GET'])
def getProductsByPrice(self):
     min_price = self.GET.get('min_price')
     max_price = self.GET.get('max_price')

     products = Product.objects.all()
     if min_price:
            products = products.filter(price__gte=min_price)
     if max_price:
            products = products.filter(price__lte=max_price)
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
     products = Product.objects.filter(user=user).order_by('-createdt')
     paginator = Paginator(products, 1)
     page = request.query_params.get('page')
     try:
         productsList = paginator.page(page)
     except PageNotAnInteger:
         productsList = paginator.page(1)
     except EmptyPage:
         productsList = paginator.page(paginator.num_pages)

     if page == None:
         page = 1

     page = int(page)
    
     serializer = ProductSerializer(products, many=True)
     return Response({'products': serializer.data, 'page': page, 'pages':paginator.num_pages })


@api_view(['POST'])
def createProduct(request):
    data = request.data

    product = Product.objects.create(
        user=request.user,
        name = data['name'],
        price = data['price'],
        brand = data['Brand'],
        condition = data['Condition'],
        location = data['location'],
        phoneNumber = data['phone'],
        
        image = request.FILES.get('selectedImage1'),
        image2 = request.FILES.get('selectedImage2'),
        image3 = request.FILES.get('selectedImage3'),
        image4 = request.FILES.get('selectedImage4'),
        descripption=data['textarea']
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
    product.phoneNumber = data['phoneNumber']
    product.descripption = data['descripption']
    #product.category = data['category']
    #product.image = request.FILES.get('image')
    #product.image2 = data['image2']
    #product.image3 = data['image3']
    #product.image4 = data['image4']
    product.save()
    serializer = ProductSerializer(product, many=False)
    product_updated.delay(product._id)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Product Deleted')

@api_view(['POST'])
def uploadImage(request):
    data = request.data
    
    product_id = data['id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()
    return Response('Image was uploaded')

@api_view(['POST'])
def uploadImage2(request):
    data = request.data
    
    product_id = data['id']
    product = Product.objects.get(_id=product_id)

    product.image2 = request.FILES.get('image2')
    product.save()
    return Response('Image was uploaded')

@api_view(['POST'])
def uploadImage3(request):
    data = request.data
    
    product_id = data['id']
    product = Product.objects.get(_id=product_id)

    product.image3 = request.FILES.get('image3')
    product.save()
    return Response('Image was uploaded')

@api_view(['POST'])
def uploadImage4(request):
    data = request.data
    
    product_id = data['id']
    product = Product.objects.get(_id=product_id)

    product.image4 = request.FILES.get('image4')
    product.save()
    return Response('Image was uploaded')

@api_view(['GET'])
def getFavorite(request):
    user = request.user.id
    favorites = Favorite.objects.filter(user=user)
    favorite_products = [favorite.product for favorite in favorites]
    serializer = ProductSerializer(favorite_products, many=True)
    return Response({'products': serializer.data})


@api_view(['POST'])
def addToFavorite(request, pk1, pk2):
    user = User.objects.get(id=pk2)
    product = Product.objects.get(_id=pk1)

    existing_favorite = Favorite.objects.filter(user=user, product=product).first()

    if existing_favorite:
        return Response('Offer already in favorites.', status=400)

    favorite = Favorite.objects.create(user=user, product=product)
    favorite.save()
    return Response('Product added to favorites.')

@api_view(['DELETE'])
def deleteFavorite(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)

    favourite = Favorite.objects.filter(user=user, product=product).first()

    if not favourite:
        return Response('product is not in favorites.', status=400)

    favourite.delete()
    return Response('product removed from favorites.')