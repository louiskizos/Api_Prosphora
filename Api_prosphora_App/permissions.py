from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta

class IsAbonnementValide(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        abonnement = getattr(user.eglise, 'abonnement', None)
        if not abonnement:
            return False

        date_fin = abonnement.date + timedelta(days=abonnement.mois * 30)
        return datetime.now().date() <= date_fin
