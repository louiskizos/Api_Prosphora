from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    # ============= Eglise ==================
    path('', Church_Mixins.as_view(), name='churches'),
    path('church_by_id/<int:pk>/', Church_Mixins.as_view(), name='church_by_id'),
    path('delete_update_church/<int:pk>/', Church_Mixins.as_view(), name='delete_update_church'),
    # ============= Utilisateur ====================
    path('register/', Register_Mixins.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('liste_user_par_eglise/<int:pk>/', Register_Mixins.as_view(), name='liste_user_par_eglise'),
    path('delete_update_user/<int:pk>/', Register_Mixins.as_view(), name='delete_update_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # ============= Token  =========================
    
    # ============= Abonnement =====================
    path('abonnement/', Abonnement_Mixins.as_view(), name='create-abonnement'),
    path('update_delete_abonnement/<int:pk>/', Abonnement_Mixins.as_view(), name='update_delete_abonnement'),
    path('liste_abonnement_par_eglise/<int:pk>/', Abonnement_Mixins.as_view(), name='liste_abonnement_par_eglise'),
]
