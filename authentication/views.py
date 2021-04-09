from .serializers import UserSerializer, ProfileSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser, FormParser


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


class ProfileView(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request):
        p = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(p)
        serializer.update(p, request.data)
        return Response(serializer.data)

    def get(self, request):
        p = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(p)
        return Response(serializer.data)


class PublicProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        username = self.request.query_params.get('username')
        u = User.objects.get(username=username)
        return Profile.objects.get(user=u)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = ProfileSerializer(queryset)
        return Response(serializer.data)
