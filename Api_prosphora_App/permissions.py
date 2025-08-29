from datetime import timedelta, datetime
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

        # Calcule la date de fin d’abonnement
        date_fin = dernier_abonnement.date + timedelta(days=dernier_abonnement.mois * 30)

        # Compare avec la date d’aujourd’hui
        return datetime.now().date() <= date_fin
