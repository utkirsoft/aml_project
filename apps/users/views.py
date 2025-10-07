from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all().values("id", "username", "email")
        return Response(users)
