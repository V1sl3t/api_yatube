from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Comment, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save(author=self.request.user)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        queryset = Comment.objects.filter(post=self.get_post())
        return queryset

    def perform_create(self, serializer):
        serializer.save(post=self.get_post(), author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied
        serializer.save(post=self.get_post(), author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied
        instance.delete()
