from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import ItemSerializer
from .models import Item
from django.http import FileResponse, Http404
from django.conf import settings
import os

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    #permission_classes = [permissions.IsAuthenticated]

def video_view(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if not os.path.exists(file_path):
        raise Http404

    response = FileResponse(open(file_path, 'rb'), content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    return response
