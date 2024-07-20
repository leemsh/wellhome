from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('Item', views.ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('video/<str:filename>/', video_view, name='video_view'),
    #path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
]