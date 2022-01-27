from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets

from posts.models import Group, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer,
                          GroupSerializer,
                          PostSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

    def check_post(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)

        return post

    def get_queryset(self):
        post = self.check_post()
        new_queryset = post.comments.all()

        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.check_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
