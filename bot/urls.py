from django.urls import path, include
from .views import FacebookBotView

urlpatterns = [
    path('fb-webhook', FacebookBotView.as_view(), name="test"),
]
