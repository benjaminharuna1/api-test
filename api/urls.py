from django.urls import path
from .views import hello_visitor


urlpatterns=[
     path('api/hello', hello_visitor, name='hello_visitor'),
]