import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from .models import Payment
from drf_spectacular.utils import extend_schema
from rest_framework import serializers

class CreatePaymentResponseSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField()
    razorpay_key = serializers.CharField()
    amount = serializers.IntegerField()
    currency = serializers.CharField()

class CreatePaymentErrorSerializer(serializers.Serializer):
    error = serializers.CharField()

@extend_schema(
    parameters=[{'name': 'order_id', 'type': 'int'}],
    responses={
        200: CreatePaymentResponseSerializer,
        400: CreatePaymentErrorSerializer
    }
)
class CreatePaymentView(APIView):
    serializer_class = None
    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)

        if order.status != 'PENDING':
            return Response(
                {'error': 'Payment already initiated'},
                status=status.HTTP_400_BAD_REQUEST
            )

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        razorpay_order = client.order.create({
            "amount": int(order.total_amount * 100),  # paise
            "currency": "INR",
            "payment_capture": 1
        })

        payment = Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order['id']
        )

        return Response({
            "razorpay_order_id": razorpay_order['id'],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": razorpay_order['amount'],
            "currency": "INR"
        })


# Payment Verification----

from razorpay.errors import SignatureVerificationError

class VerifyPaymentSuccessSerializer(serializers.Serializer):
    message = serializers.CharField()

class VerifyPaymentErrorSerializer(serializers.Serializer):
    error = serializers.CharField()

@extend_schema(
    responses={
        200: VerifyPaymentSuccessSerializer,
        400: VerifyPaymentErrorSerializer
    }
)

class VerifyPaymentView(APIView):
    serializer_class = None
    def post(self, request):
        data = request.data

        try:
            payment = Payment.objects.get(
                razorpay_order_id=data['razorpay_order_id']
            )

            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            payment.razorpay_payment_id = data['razorpay_payment_id']
            payment.razorpay_signature = data['razorpay_signature']
            payment.is_paid = True
            payment.save()

            payment.order.status = 'PAID'
            payment.order.save()
            
            payment.meta = {
                "razorpay_order_id": data['razorpay_order_id'],
                "razorpay_payment_id": data['razorpay_payment_id'],
                "status": "SUCCESS"
                }
            payment.save()


            return Response({'message': 'Payment successful'})

        except SignatureVerificationError:
            return Response(
                {'error': 'Payment verification failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
