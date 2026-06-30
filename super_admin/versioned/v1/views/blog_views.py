from rest_framework.views import APIView
from django.shortcuts import get_list_or_404,get_object_or_404
from super_admin.models.blog_model import (
    Blog,
    BlogCategory,
)
from super_admin.versioned.v1.serializers.blog_serializer import (
    BlogCategorySerializer,
    BlogSerializer,
)
from core.helpers.custom_pagination import (
    CustomPageNumberPagination
)
from core.helpers.custom_response_hander import (
    CustomResponse
)
from core.utils.common_models import (
    BaseAPIView
)
from core.helpers.permissions import (
    IsAdmin,
    IsStudent,
    IsMentor,
    IsAdminOrMentor,
    IsAdminOrStudent,
    IsVerifiedUser
)


class BlogCategoryCreateAPIView(BaseAPIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = BlogCategorySerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Blog categories created successfully.",
            data=serializer.data
        )
    
    def get(self,request):

        queryset=BlogCategory.objects.filter(is_active=True).order_by("-created_at")

        search = request.GET.get("search")

        if search:
            queryset = queryset.filter(name__icontains=search)

        paginator, paginated_categories = self.paginate_queryset(queryset,request)

        serializer = BlogCategorySerializer(paginated_categories,many=True,context={"request": request})

        paginated_response = paginator.get_paginated_response(serializer.data)

        return CustomResponse.success(
            message="Blog Categories fetched successfully.",
            data=paginated_response.data
        )
    

class BlogCategoryDetailAPIView(BaseAPIView):

    permission_classes = [IsAdmin]
    def get(self, request, id):

        blog_cat_object=get_object_or_404(BlogCategory,pk=id,is_active=True)

        serializer = BlogCategorySerializer(blog_cat_object,context={"request": request})

        return CustomResponse.success(
            message="Blog Category fetched successfully.",
            data=serializer.data
        )
    
    def put(self, request, id):

        blog_cat_object=get_object_or_404(BlogCategory,pk=id,is_active=True)

        serializer = BlogCategorySerializer(blog_cat_object,data=request.data,partial=True)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Blog Category updated successfully.",
            data=serializer.data
        )
    
    def delete(self, request, id):

        blog_object=get_object_or_404(BlogCategory,pk=id,is_active=True)

        blog_object.delete()

        return CustomResponse.success(
            message="Blog deleted successfully.",
            data={}
        )



class BlogCreateAPIView(BaseAPIView):

    permission_classes = [IsAdmin]

    def post(self, request):

        serializer = BlogSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(author=request.user)

        return CustomResponse.success(
            message="Blog created successfully.",
            data=serializer.data
        )
    
    def get(self,request):
        
        queryset=Blog.objects.filter(is_active=True).order_by("-created_at")

        search = request.GET.get("search")
        category = request.GET.get("category")
        published = request.GET.get("published")
        featured = request.GET.get("featured")

        if search:
            queryset = queryset.filter(title__icontains=search)

        if category:
            queryset = queryset.filter(category_id=category)

        if published:
            queryset = queryset.filter(is_published=published.lower() == "true")

        if featured:
            queryset = queryset.filter(is_featured=featured.lower() == "true")

        if search:
            queryset = queryset.filter(title__icontains=search)

        paginator, paginated_categories = self.paginate_queryset(queryset,request)

        serializer = BlogSerializer(paginated_categories,many=True,context={"request": request})

        paginated_response = paginator.get_paginated_response(serializer.data)

        return CustomResponse.success(
            message="Blog fetched successfully.",
            data=paginated_response.data
        )
    
class BlogDetailAPIView(APIView):


    def get(self,request,blog_id):

        blog_object = get_object_or_404(Blog,pk=blog_id,is_active=True)

        serializer = BlogSerializer(blog_object,context={"request": request})

        return CustomResponse.success(
            message="Blog fetched successfully.",
            data=serializer.data
        )
    

    def put(self, request, blog_id):
        
        blog_object = get_object_or_404(Blog,pk=blog_id,is_active=True)

        serializer = BlogSerializer(blog_object,data=request.data,partial=True)

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return CustomResponse.success(
            message="Blog Updated successfully.",
            data=serializer.data
        )
    
    def delete(self,request,blog_id):
        
        blog_object = get_object_or_404(Blog,pk=blog_id,is_active=True)

        blog_object.delete()

        return CustomResponse.success(
            message="Blog Deleted successfully.",
            data={}
        )