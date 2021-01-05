from django.urls import path
from apps.users.views import *
urlpatterns = [
    # path('username/<username>/count/', UsernameCountView.as_view()),
    path('usernames/<uc:username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mb:mobile>/count/', MobileCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]