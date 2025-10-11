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
    
# ============= Abonnement =====================
    path('abonnement/', Abonnement_Mixins.as_view(), name='create-abonnement'),
    path('update_delete_abonnement/<int:pk>/', Abonnement_Mixins.as_view(), name='update_delete_abonnement'),
    path('liste_abonnement_par_eglise/<int:pk>/', Abonnement_Mixins.as_view(), name='liste_abonnement_par_eglise'),

# ============= Groupe des offrandes ====================
    path('groupe_offrande/', Groupe_Offrandes_Mixins.as_view(), name='create-groupe_offrande'),
    path('delete_groupe_offrande/<str:pk>/', Groupe_Offrandes_Mixins.as_view(), name='delete_groupe_offrande'),
    path('update_groupe_offrande/<str:pk>/', Groupe_Offrandes_Mixins.as_view(), name='update_groupe_offrande'),

# ============= Sorte_Offrande ====================

    path('offrande/', Offrande_Mixins.as_view(), name='create-offrande'),
    path('delete_offrande/<int:pk>/', Offrande_Mixins.as_view(), name='delete_offrande'),
    path('update_offrande/<int:pk>/', Offrande_Mixins.as_view(), name='update_offrande'),
    path('liste_offrande_par_eglise/<int:pk>/', Offrande_Mixins.as_view(), name='liste_offrande_par_eglise'),
    path('liste_offrande_par_groupe/<str:pk>/', Offrande_Mixins.as_view(), name='liste_offrande_par_groupe'),
    path('liste_offrande_par_eglise_et_groupe/<int:pk>/<str:grp>/', Offrande_Mixins.as_view(), name='liste_offrande_par_eglise_et_groupe'),
    path('total_offrande_par_eglise/<int:pk>/', Offrande_Mixins.as_view(), name='total_offrande_par_eglise'),


# ============= Payement Offrande ====================
    path('payement_offrande/', Payement_Offrande_Mixins.as_view(), name='create-payement_offrande'),
    path('delete_payement_offrande/<str:pk>/', Payement_Offrande_Mixins.as_view(), name='delete_payement_offrande'),
    path('update_payement_offrande/<str:pk>/', Payement_Offrande_Mixins.as_view(), name='update_payement_offrande'),

# ============= Groupe Previsions   ====================
    path('groupe_prevision/', Groupe_Previsions_Mixins.as_view(), name='create-groupe_prevision'),
    path('delete_groupe_prevision/<str:pk>/', Groupe_Previsions_Mixins.as_view(), name='delete_groupe_prevision'),
    path('update_groupe_prevision/<str:pk>/', Groupe_Previsions_Mixins.as_view(), name='update_groupe_prevision'),
# ============= Prevoir ====================
    path('prevoir/', Prevoir_Mixins.as_view(), name='create-prevoir'),
    path('delete_prevoir/<str:pk>/', Prevoir_Mixins.as_view(), name='delete_prevoir'),
    path('update_prevoir/<str:pk>/', Prevoir_Mixins.as_view(), name='update_prevoir'),
    path('liste_prevoir_par_eglise/<int:pk>/', Prevoir_Mixins.as_view(), name='liste_prevoir_par_eglise'),
    path('total_prevoir_par_eglise/<str:pk>/', Prevoir_Mixins.as_view(), name='total_prevoir_par_eglise'),



]
