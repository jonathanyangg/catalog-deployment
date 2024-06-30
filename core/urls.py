from django.urls import path
from . import views
# from .views import test_env_vars

urlpatterns = [
    path('', views.index, name = 'index'),
    # path('test_env_vars/', test_env_vars, name='test_env_vars'),
]