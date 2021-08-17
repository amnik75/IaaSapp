from django.conf.urls import url
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
        path('api/', include('vmCreation.api.urls')),
        url('', views.status),
        url('status/', views.status),
        url('status', views.status),

]
