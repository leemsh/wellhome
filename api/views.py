from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ItemSerializer
from .models import Item
from django.http import FileResponse, Http404
from django.conf import settings
import os

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

def video_view(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'videos', filename)  # 'videos' 폴더를 추가
    if not os.path.exists(file_path):
        raise Http404

    response = FileResponse(open(file_path, 'rb'), content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    response.file_to_stream = open(file_path, 'rb')  # 파일 경로를 response 객체에 추가
    return response