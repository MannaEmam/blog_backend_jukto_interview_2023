from blog.models import Post, Comment
from blog.api import PostSerializer, CommentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from authentication.permissions.permission import IsAdminOwnModOrRead, IsAdminOwnOrRead
from django_filters.rest_framework import DjangoFilterBackend
from blog.utils import PostSearchFilter, PostFilterSet


class Post(viewsets.ModelViewSet):
    permission_classes = [IsAdminOwnModOrRead, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, PostSearchFilter]
    filterset_class = PostFilterSet
    search_fields = ['author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"extra_data": self.request.query_params.get('extra_data', False)})
        return context


class Comment(viewsets.ModelViewSet):
    permission_classes = [IsAdminOwnOrRead, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
