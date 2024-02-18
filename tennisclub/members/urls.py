from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', include('members.urls')),
    path('admin/', admin.site.urls),
]
