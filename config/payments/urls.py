from django.urls import path
from .views import CreatePaymentView, VerifyPaymentView

urlpatterns = [
    path('payments/create/<int:order_id>/', CreatePaymentView.as_view()),
    path('payments/verify/', VerifyPaymentView.as_view()),
]
