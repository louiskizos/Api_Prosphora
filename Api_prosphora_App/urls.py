from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView, RegisterView, ChurchListView, AbonnementCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    # JWT token (custom view to return extra data)
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('churches/', ChurchListView.as_view(), name='churches'),
    path('abonnement/', AbonnementCreateView.as_view(), name='create-abonnement'),
]
