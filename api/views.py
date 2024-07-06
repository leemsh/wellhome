from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import ItemSerializer
from .models import Item

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    #permission_classes = [permissions.IsAuthenticated]