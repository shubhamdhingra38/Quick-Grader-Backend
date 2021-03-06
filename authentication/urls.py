from django.urls import path
from .views import ProfileView, PublicProfileView, UserInstanceView
from .views import UserView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'users', UserView)
urlpatterns = router.urls


urlpatterns += [
    path('user/', UserInstanceView.as_view()),
    path('token/', obtain_auth_token),
    path('profile/', ProfileView.as_view()),
    path('view-profile', PublicProfileView.as_view()),
]
