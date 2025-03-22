from django.shortcuts import render
import statistics
from rest_framework import viewsets

# Create your views here.
from django.http import HttpResponse

from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = User.objects.filter(id=id)
            return queryset
        else:
            return User.objects.all()
