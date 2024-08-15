from django.urls import path
from . import views
# from .views import test_env_vars

urlpatterns = [
    path('', views.index, name = 'index'),
]