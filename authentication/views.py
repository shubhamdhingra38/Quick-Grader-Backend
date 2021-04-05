from .serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import viewsets, mixins


class UserView(mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    # authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]


class UserInstanceView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication, BasicAuthentication]

    def get(self, request):
        p = Profile.objects.get(user=request.user)
        serializer = UserSerializer(p)
        return Response(serializer.data)
