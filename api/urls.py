from django.urls import path
from rest_framework import routers

from api import views

router = routers.SimpleRouter()
router.register('jobs', views.JobViewSet)


urlpatterns = [
    path('create_load/', views.CreateLoadView.as_view())
] + router.urls
