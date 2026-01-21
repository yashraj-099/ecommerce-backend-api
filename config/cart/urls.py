from django.urls import path
from .views import (
    CartDetailView,
    AddToCartView,
    UpdateCartItemView,
    RemoveCartItemView
)

urlpatterns = [
    path('cart/', CartDetailView.as_view()),
    path('cart/add/', AddToCartView.as_view()),
    path('cart/item/<int:item_id>/', UpdateCartItemView.as_view()),
    path('cart/item/<int:item_id>/remove/', RemoveCartItemView.as_view()),
]
