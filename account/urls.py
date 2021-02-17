from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.views import registration_view
from . import views
app_name = 'account'





urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('login', views.MyTokenObtain.as_view()),
    path('jwt_test/refresh', TokenRefreshView.as_view()),
    path('register', registration_view, name="register"),
    path('activities', views.ActivitiesView.as_view()),
]