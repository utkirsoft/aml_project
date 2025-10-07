from django.urls import path
from .views import PersonDetailsAPIView

urlpatterns = [
    path('person/details/', PersonDetailsAPIView.as_view(), name='person-details'),
]