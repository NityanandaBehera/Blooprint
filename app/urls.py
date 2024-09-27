from django.urls import path
from app.views import *

urlpatterns = [
    path('signup/',UserRegistration.as_view(),name="signup"),
    path('signin/',UserLoginView.as_view(),name="login"),
    path('items/', ItemCreateView.as_view(), name='item-create'), 
    path('items/all/', ItemListView.as_view(), name='item-list'), 
    path('items/<int:item_id>/', ItemDetailView.as_view(), name='item-detail'),  
    path('items/<int:item_id>/', ItemUpdateView.as_view(), name='item-update'), 
    path('items/<int:item_id>/', ItemDeleteView.as_view(), name='item-delete'),
]
