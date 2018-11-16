from django.urls import path
from .views import *

urlpatterns = [
    path('api/v_1/', CategoryList.as_view())
]