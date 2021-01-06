from django.urls import path
from apps.areas.views import ProvienceView
urlpatterns = [
    path('areas/', ProvienceView.as_view()),
]