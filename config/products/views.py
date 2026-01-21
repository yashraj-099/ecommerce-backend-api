from rest_framework import viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from users.permissions import ReadOnlyForCustomer
from .filters import ProductFilter
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyForCustomer]

@extend_schema_view(
    retrieve=extend_schema(parameters=[{'name': 'pk', 'type': 'int'}]),
    update=extend_schema(parameters=[{'name': 'pk', 'type': 'int'}]),
    partial_update=extend_schema(parameters=[{'name': 'pk', 'type': 'int'}]),
    destroy=extend_schema(parameters=[{'name': 'pk', 'type': 'int'}]),
)
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny, ReadOnlyForCustomer]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'id']

    def get_queryset(self):
        user = self.request.user

        queryset = (
            Product.objects
            .filter(is_active=True)
            .select_related('category', 'created_by')
        )

        if getattr(self, 'swagger_fake_view', False):
            return queryset

        if user.is_authenticated and user.role == 'SELLER':
            queryset = queryset.filter(created_by=user)

        return queryset


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()
