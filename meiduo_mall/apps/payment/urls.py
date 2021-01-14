from django.urls import path
from . import views
urlpatterns = [
    path('payment/<order_id>/', views.PayURLView.as_view()),
]