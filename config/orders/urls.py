from django.urls import path
from .views import CreateOrderView, MyOrdersView

urlpatterns = [
    path('orders/create/', CreateOrderView.as_view()),
    path('orders/my-orders/', MyOrdersView.as_view()),
]
