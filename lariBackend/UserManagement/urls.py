from django.urls import path
from .views import Register, CustomTokenObtainPairView, CustomTokenRefreshView, VerifyUser

urlpatterns = [
    path('register', Register.as_view()),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify-user', VerifyUser.as_view(), name='verify-user'),
]