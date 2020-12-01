from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('test/', include('quiz.urls')),
    path('ml/', include('ml.urls')),
    # path('', TemplateView.as_view(template_name='index.html')),
]

#https://stackoverflow.com/questions/40826295/react-routing-and-django-url-conflict
# urlpatterns += [
#     # re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name="index.html")), 
# ]