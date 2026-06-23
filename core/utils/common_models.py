from django.db import models
from django.utils import timezone
import uuid
from rest_framework.views import APIView
from core.helpers.custom_pagination import (
    CustomPageNumberPagination
)
class CommonModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    is_active =  models.BooleanField(default=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
class BaseAPIView(APIView):
    pagination_class = CustomPageNumberPagination

    def paginate_queryset(self, queryset, request):
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(
            queryset,
            request
        )
        return paginator, paginated_queryset