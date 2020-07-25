from django.shortcuts import get_object_or_404
from posts.models import Post, Comment, Group, Follow
from rest_framework import permissions, viewsets, filters

from .permissions import IsAuthorOrReadOnly, IsFollowerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group', None)
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get("post_id"))


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsFollowerOrReadOnly, permissions.IsAuthenticatedOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username', ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
