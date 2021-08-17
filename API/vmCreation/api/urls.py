from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
        url('create/', views.Create.as_view()),
        url('create', views.Create.as_view()),
]

