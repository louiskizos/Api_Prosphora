from datetime import timedelta, datetime
from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission



class IsAbonnementValide(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Récupère le dernier abonnement lié à l'église
        dernier_abonnement = user.eglise.abonnements.order_by('-date').first()
        if not dernier_abonnement:
            return False

        date_fin = dernier_abonnement.date + timedelta(days=dernier_abonnement.mois * 30)

        return datetime.now().date() <= date_fin



class IsSameChurch(BasePermission):

    def has_object_permission(self, request, view, obj):

        return hasattr(obj, 'eglise') and obj.eglise == request.user.eglise
