from django.shortcuts import render
from rest_framework import viewsets

from users.models import Profile
from .models import Post
from .serializers import PostSerializer, PostCreateSerializer
from .permissions import CustomReadOnly
# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [CustomReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return PostSerializer

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)
