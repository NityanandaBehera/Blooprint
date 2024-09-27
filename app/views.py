from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers import UserRegistrationSerializer,UserLoginSerializer,ItemSerializer
from django.contrib.auth import authenticate
from app.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Item
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.cache import cache


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# Create your views here.
class UserRegistration(APIView):
    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            # token=get_tokens_for_user(user)
            return Response({'msg':"Registration successfully"})    
        return Response(serializer.errors)
    
class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=UserLoginSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(request,email=email,password=password)
            print(user)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':"User login successfully"})
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}})
        return Response(serializer.errors) 

class ItemCreateView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            if Item.objects.filter(name=serializer.validated_data['name']).exists():
                return Response({"error": "Item already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ItemDetailView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self, request, item_id):
        # Check if the item is cached in Redis
        cache_key = f'item_{item_id}'
        cached_item = cache.get(cache_key)

        if cached_item:
            # print("data getting from cache")
            return Response(cached_item, status=status.HTTP_200_OK)

        # If the item is not cached, fetch it from the database
        item = get_object_or_404(Item, pk=item_id)
        serializer = ItemSerializer(item)

        # Cache the serialized item data in Redis (e.g., for 10 minutes)
        cache.set(cache_key, serializer.data, timeout=60*10)

        return Response(serializer.data, status=status.HTTP_200_OK)
class ItemListView(APIView):
    def get(self, request):
        # Try to fetch cached data
        cached_items = cache.get('all_items')
        if cached_items:
            # print("data geting from cache")
            return Response(cached_items, status=status.HTTP_200_OK)
        
        # If cache is empty, query the database and store the result in the cache
        print("data geting from db")
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        cache.set('all_items', serializer.data, timeout=60*1)  # Cache for 5 minutes
        return Response(serializer.data, status=status.HTTP_200_OK)

# 4. Update Item Endpoint
class ItemUpdateView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def put(self, request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 5. Delete Item Endpoint
class ItemDeleteView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def delete(self, request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        item.delete()
        return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)