from rest_framework.views import APIView
from .serializer import *
from .models import *
from rest_framework import generics, mixins, status
from .permissions import IsAbonnementValide, IsSameChurch
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Q, OuterRef, Subquery, Sum, DecimalField, BigIntegerField, F, ExpressionWrapper, Value
from decimal import Decimal
from django.db.models.functions import Coalesce, ExtractYear, Cast
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import os
from django.http import FileResponse
from django.core import management
import tempfile



def backup_json_view(request, eglise_id):

    try:
        eglise = Church.objects.get(pk=eglise_id)
    except Church.DoesNotExist:
        return FileResponse(status=404)

    nom_eglise = eglise.nom.replace(" ", "_")
    date_str = timezone.now().strftime("%Y-%m-%d")
    filename = f"{nom_eglise}_{date_str}_backup.json"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        management.call_command('dumpdata', '--indent=2', f'--output={tmp.name}')
        tmp.flush()
        response = FileResponse(
            open(tmp.name, 'rb'),
            as_attachment=True,
            filename=filename
        )

    os.unlink(tmp.name)
    return response




class Register_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
    ):
    

    queryset = App_user.objects.all()
    serializer_class = RegisterSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return App_user.objects.filter(pk=pk)
        return App_user.objects.all()
    
    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):

        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)



@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):

    def get(self, request):
        return Response(
            {"message": "Utilisez POST pour vous connecter."},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        num_phone = request.data.get("num_phone")
        password = request.data.get("password")

        if not num_phone or not password:
            return Response({"error": "Numéro de téléphone et mot de passe requis."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, num_phone=num_phone, password=password)

        if user is not None:
            login(request, user)

            dernier_abonnement = (
                user.eglise.abonnements.order_by('-date').first()
                if hasattr(user, "eglise") and user.eglise else None
            )

            return Response({
                "user_id": user.id,
                "nom": user.nom,
                "num_phone": user.num_phone,
                "role": user.role,
                "eglise": user.eglise.nom if user.eglise else None,
                "id_eglise": user.eglise.id if hasattr(user, "eglise") and user.eglise else None,
                "abonnement_mois": dernier_abonnement.mois if dernier_abonnement else None,
                "abonnement_date": dernier_abonnement.date if dernier_abonnement else None
            }, status=status.HTTP_200_OK)

        return Response({"error": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    
    def post(self, request):
        logout(request)
        return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK)



class Church_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
    ):
    
    queryset = Church.objects.all()
    serializer_class = ChurchSerializer
    lookup_field = 'pk'
    
    
    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
            pk = self.kwargs.get('pk')
            if pk:
                return Church.objects.filter(pk=pk)
            return Church.objects.all()
    

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Église créée avec succès.", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs, partial=True)

    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)


# ====================== Abonnement =========================

class Abonnement_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):

   # permission_classes = [IsAuthenticated]


    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        id_eglise = self.kwargs.get('id_eglise')
        pk = self.kwargs.get('pk')

        queryset = Abonnement.objects.all()

        if id_eglise:
            queryset = queryset.filter(eglise_id=id_eglise)
        if pk:
            queryset = queryset.filter(pk=pk)

        return queryset
    # def get_queryset(self):

    #     user = self.request.user
    #     eglise_id = self.kwargs.get('eglise_id', None)

    #     if eglise_id:
    #         return Abonnement.objects.filter(user__eglise_id=eglise_id)

    #     if hasattr(user, "eglise") and user.eglise:
    #         return Abonnement.objects.filter(user__eglise=user.eglise)

    #     return Abonnement.objects.none()




    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = AbonnementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Abonnement créé."})
        return Response(serializer.errors, status=400)
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)

    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)

# ======================== GROUPE OFFRANDE =========================
class Groupe_Offrandes_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):
    queryset = Groupe_Offrandes.objects.all()
    serializer_class = Groupe_OffrandesSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        eglise_id = self.kwargs.get('eglise_id')
        if eglise_id:
            return Groupe_Offrandes.objects.filter(user__eglise_id=eglise_id)
        return Groupe_Offrandes.objects.none()

    def get_serializer_context(self):
        
        context = super().get_serializer_context()
        context['eglise_id'] = self.kwargs.get('eglise_id')
        return context

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
# ======================== SORTE OFFRANDE =========================

class Offrande_Mixins(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
  # permission_classes = [IsAuthenticated, IsSameChurch]
    serializer_class = Sorte_OffrandeSerializer
    queryset = Sorte_Offrande.objects.all()
    lookup_field = 'pk'


    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get('pk')
        grp = self.kwargs.get('grp')

        eglise_id = self.kwargs.get('eglise_id') or self.request.query_params.get('eglise_id')

        if eglise_id:

            queryset = Sorte_Offrande.objects.filter(
                descript_recette__user__eglise_id=eglise_id
            ).select_related('descript_recette')
        else:

            queryset = Sorte_Offrande.objects.filter(
                descript_recette__user__eglise=user.eglise
            ).select_related('descript_recette')

        if pk:
            queryset = queryset.filter(pk=pk)
        if grp:
            queryset = queryset.filter(descript_recette__id=grp)

        return queryset


    def get(self, request, *args, **kwargs):
        
        pk = kwargs.get('pk')
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Offrande créée avec succès.", "data": serializer.data},
                        status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)


    def delete(self, request, *args, **kwargs):
        """
        Suppression d'une offrande.
        """
        return self.destroy(request, *args, **kwargs)
    
# ======================== GROUPE PREVISION =========================

class Groupe_Previsions_Mixins(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = Groupe_Previsions.objects.all()
    serializer_class = Groupe_PrevisionsSerializer
    lookup_field = 'pk'

    def get_queryset(self):

        eglise_id = self.kwargs.get('eglise_id')
        if eglise_id:
            return Groupe_Previsions.objects.filter(user__eglise_id=eglise_id)
        return Groupe_Previsions.objects.all()

    def get_serializer_context(self):

        context = super().get_serializer_context()
        context['eglise_id'] = self.kwargs.get('eglise_id')
        return context

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        eglise_id = kwargs.get('eglise_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  
        return Response(
            {"message": f"Groupe de prévision créé pour l’église {eglise_id}.", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    def patch(self, request, *args, **kwargs):
        """PATCH : mise à jour partielle"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """DELETE : suppression"""
        return self.destroy(request, *args, **kwargs)
    
# ======================== PREVOIR =========================
class Prevoir_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):
    queryset = Prevoir.objects.all()
    serializer_class = PrevoirSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        eglise_id = self.kwargs.get('eglise_id')
        if eglise_id:
            return Prevoir.objects.filter(descript_prevision__user__eglise_id=eglise_id)
        return Prevoir.objects.none()

    def get_serializer_context(self):
        
        context = super().get_serializer_context()
        context['eglise_id'] = self.kwargs.get('eglise_id')
        return context

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Prévoir créé.", "data": serializer.data}, status=201)

    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# ======================== PAYEMENT =========================

class Payement_Offrande_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):
    queryset = Payement_Offrande.objects.all()
    serializer_class = PayementOffrandeSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get('pk')
        eglise_id = self.kwargs.get('eglise_id')

        queryset = Payement_Offrande.objects.all()

        if eglise_id:
            queryset = queryset.filter(
                nom_offrande__descript_recette__user__eglise_id=eglise_id
            )
        elif getattr(user, "is_authenticated", False) and hasattr(user, "eglise") and user.eglise:
            queryset = queryset.filter(
                nom_offrande__descript_recette__user__eglise=user.eglise
            )
        else:
            queryset = Payement_Offrande.objects.none()

        if pk:
            queryset = queryset.filter(pk=pk)

        return queryset

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        # 🔒 On remplace retrieve() de DRF
        if pk:
            instance = self.get_queryset().first()
            if not instance:
                return Response({"detail": "Not found"}, status=404)

            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Payement créé."})

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)


# ======================== AHADI =========================

class Ahadi_Mixins(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    serializer_class = AhadiSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        eglise_id = self.kwargs.get('eglise_id')
        if not eglise_id:
            return Ahadi.objects.none()
        return Ahadi.objects.filter(nom_offrande__descript_recette__user__eglise_id=eglise_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Subquery pour total payé
        paiements = Payement_Offrande.objects.filter(
            type_payement="in",
            nom_offrande=OuterRef('nom_offrande'),
            departement=OuterRef('nom_postnom'),
        ).filter(
            Q(nom_offrande__descript_recette__description_recette="Les engagement des adhérents") |
            Q(nom_offrande__descript_recette__description_recette="LES ENGAGEMENTS DES ADHERENTS")
        ).values('nom_offrande', 'departement').annotate(
            total=Sum('montant')
        ).values('total')

        queryset = queryset.annotate(
            total_paye=Subquery(paiements, output_field=DecimalField(max_digits=15, decimal_places=2))
        )

        # Calcul du reste
        for obj in queryset:
            obj.reste = (obj.montant or 0) - (obj.total_paye or 0)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "ahadi_data": serializer.data,
        }, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Ahadi créé.", "data": serializer.data}, status=201)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



# ======================== ETAT DE BESOIN =========================

class EtatBesoin_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):
    queryset = EtatBesoin.objects.all()
    serializer_class = EtatBesoinSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        # On récupère l'ID de l'église si présent
        eglise_id = self.kwargs.get('eglise_id') or self.request.query_params.get('eglise_id')

        # Si on liste (pas de pk dans kwargs), filtrer par eglise_id
        if 'pk' not in self.kwargs and eglise_id:
            return EtatBesoin.objects.filter(user__eglise_id=eglise_id)

        # Pour retrieve, update, delete : ne pas filtrer par eglise_id
        return EtatBesoin.objects.all()

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Etat de besoin créé.", "data": serializer.data}, status=201)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
# ======================== 40 % =========================
from django.db.models import Max, DateTimeField


class Quarante_Pourcent_Mixins(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    serializer_class = Quarante_PourcentSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        eglise_id = self.kwargs.get('eglise_id')
        if not eglise_id:
            return Quarante_Pourcent.objects.none()

        return Quarante_Pourcent.objects.filter(
            nom_offrande__descript_recette__user__eglise_id=eglise_id
        )


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        paiements_total = Payement_Offrande.objects.filter(
            type_payement="in",
            nom_offrande=OuterRef('nom_offrande'),
        ).values('nom_offrande').annotate(
            total=Sum('montant')
        ).values('total')

        derniere_date = Payement_Offrande.objects.filter(
            type_payement="in",
            nom_offrande=OuterRef('nom_offrande')
        ).values('nom_offrande').annotate(
            derniere=Max('date_payement')
        ).values('derniere')

        queryset = queryset.annotate(
            total_paye=Coalesce(
                Subquery(
                    paiements_total,
                    output_field=DecimalField(max_digits=15, decimal_places=2)
                ),
                Value(Decimal('0.00'), output_field=DecimalField(max_digits=15, decimal_places=2))
            ),

            quarante_pourcent=ExpressionWrapper(
                F('total_paye') * Value(
                    Decimal('0.40'),
                    output_field=DecimalField(max_digits=5, decimal_places=2)
                ),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            ),

            derniere_date_payement=Subquery(
                derniere_date,
                output_field=DateTimeField()
            )
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"data": serializer.data},
            status=status.HTTP_200_OK
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {"data": serializer.data},
            status=status.HTTP_200_OK
        )
    
    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()

    #     # 🔹 Total payé par offrande
    #     paiements_total = Payement_Offrande.objects.filter(
    #         type_payement="in",
    #         nom_offrande=OuterRef('nom_offrande'),
    #     ).values('nom_offrande').annotate(
    #         total=Sum('montant')
    #     ).values('total')

    #     # 🔹 Annotation 40 %
    #     queryset = queryset.annotate(
    #         total_paye=Coalesce(
    #             Subquery(
    #                 paiements_total,
    #                 output_field=DecimalField(max_digits=15, decimal_places=2)
    #             ),
    #             Value(Decimal('0.00'), output_field=DecimalField(max_digits=15, decimal_places=2))
    #         ),
    #         quarante_pourcent=ExpressionWrapper(
    #             F('total_paye') * Value(
    #                 Decimal('0.40'),
    #                 output_field=DecimalField(max_digits=5, decimal_places=2)
    #             ),
    #             output_field=DecimalField(max_digits=15, decimal_places=2)
    #         )
    #     )

    #     # 🔹 Somme de tous les 40 %
    #     total_quarante = queryset.aggregate(
    #         somme_quarante=Coalesce(Sum('quarante_pourcent'), Value(Decimal('0.00')))
    #     )['somme_quarante']

    #     serializer = self.get_serializer(queryset, many=True)

    #     return Response(
    #         {
    #             "data": serializer.data,
    #             "total_quarante": str(total_quarante)  # string pour JSON
    #         },
    #         status=status.HTTP_200_OK
    #     )


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Quarante pourcent créé.", "datas": serializer.data}, status=201)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs, partial=True)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



# ======================== Rapport Bilan =========================   


class BilanAPIView(APIView):

    def get(self, request, eglise_id, *args, **kwargs):
        # --- Prévisions ---
        prevision_qs = (
            Prevoir.objects
            .select_related('descript_prevision')
            .filter(descript_prevision__user__eglise_id=eglise_id)
        )

        # --- Paiements ---
        paiement_qs = (
            Payement_Offrande.objects
            .select_related('nom_offrande')
            .filter(nom_offrande__descript_recette__user__eglise_id=eglise_id)
        )

        # --- Regrouper les prévisions ---
        grouped_previsions = (
            prevision_qs.annotate(annee=ExtractYear('date_prevus'))
            .values(
                'descript_prevision__num_ordre',
                'descript_prevision__description_prevision',
                'annee'
            )
            .annotate(
                total_prevus=Coalesce(
                    Sum('montant_prevus'),
                    Decimal('0.00'),
                    output_field=DecimalField()
                )
            )
            .order_by('descript_prevision__num_ordre', 'annee')
        )

        # --- Totaux paiements par compte, devise, année ---
        paiement_totals_by_currency = (
            paiement_qs.annotate(
                annee_payement=ExtractYear('date_payement'),
                compte_rapprochement=Cast(
                    'nom_offrande__num_compte', output_field=BigIntegerField()
                )
            )
            .values(
                'compte_rapprochement',
                'annee_payement',
                'type_monaie',
                'nom_offrande__nom_offrande'
            )
            .annotate(
                total_recette=Coalesce(
                    Sum('montant', filter=Q(type_payement='in')),
                    Decimal('0.00'),
                    output_field=DecimalField()
                ),
                total_depense=Coalesce(
                    Sum('montant', filter=Q(type_payement='out')),
                    Decimal('0.00'),
                    output_field=DecimalField()
                )
            )
        )

        payments_dict = {}
        for item in paiement_totals_by_currency:

            compte_cle = str(item['compte_rapprochement']).lstrip('0')
            key = (compte_cle, item['annee_payement'])

            if key not in payments_dict:
                payments_dict[key] = {
                    'libelle': item['nom_offrande__nom_offrande'],
                    'par_devise': {}
                }

            payments_dict[key]['par_devise'][item['type_monaie']] = {
                'recette': item['total_recette'],
                'depense': item['total_depense'],
            }

        combined_data = []

        for group in grouped_previsions:
            num_ordre = group['descript_prevision__num_ordre']
            annee = group['annee']

            related_previsions = prevision_qs.filter(
                descript_prevision__num_ordre=num_ordre,
                date_prevus__year=annee
            ).values('nom_prevision', 'num_compte', 'montant_prevus')

            num_comptes = list({int(c) for c in related_previsions.values_list('num_compte', flat=True)})

            prevision_list = []
            paiement_list = []
            current_totals = {'recettes': {}, 'depenses': {}}

            for item in related_previsions:
                prevision_list.append({
                    'libelle': item['nom_prevision'],
                    'num_compte': item['num_compte'],
                    'recette': '-',
                    'depense': '-',
                    'prevision': item['montant_prevus'],
                })

            for compte in num_comptes:
                compte_cle = str(compte).lstrip('0')
                key = (compte_cle, annee)
                payment_data = payments_dict.get(key)

                if payment_data:
                    for devise, totaux in payment_data['par_devise'].items():
                        recette = totaux['recette']
                        depense = totaux['depense']

                        if recette > 0 or depense > 0:
                            paiement_list.append({
                                'libelle': f"{payment_data['libelle']} ({devise})",
                                'num_compte': compte,
                                'recette': recette,
                                'depense': depense,
                                'prevision': '-',
                            })


                            current_totals['recettes'][devise] = current_totals['recettes'].get(devise, Decimal('0.00')) + recette
                            current_totals['depenses'][devise] = current_totals['depenses'].get(devise, Decimal('0.00')) + depense

            combined_data.append({
                'num_ordre': num_ordre,
                'description_prevision': group['descript_prevision__description_prevision'],
                'annee_prevus': annee,
                'total_prevus': group['total_prevus'],
                'total_recettes_par_devise': {
                    k: v for k, v in current_totals['recettes'].items() if v > 0
                },
                'total_depenses_par_devise': {
                    k: v for k, v in current_totals['depenses'].items() if v > 0
                },
                'lignes': prevision_list + paiement_list
            })

        return Response({'bilan_data': combined_data}, status=200)
    
# =================== Rapport livre de caisse =======================================


class LivreCaisseAPIView(APIView):

    #permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        user = request.user
        eglise_id = kwargs.get('eglise_id')

      
        if eglise_id:
            data_queryset = Payement_Offrande.objects.filter(
                nom_offrande__descript_recette__user__eglise_id=eglise_id
            ).order_by('type_monaie', 'date_payement')
        elif hasattr(user, "eglise") and user.eglise:
            data_queryset = Payement_Offrande.objects.filter(
                nom_offrande__descript_recette__user__eglise=user.eglise
            ).order_by('type_monaie', 'date_payement')
        else:
            return Response({"error": "Aucune église associée à l’utilisateur."}, status=400)

        
        cumulative_sums_by_currency = {}
        processed_data = []

        for item in data_queryset:
            monnaie = item.type_monaie
            montant = item.montant or 0
            cumulative_sums_by_currency[monnaie] = cumulative_sums_by_currency.get(monnaie, 0)
            cumulative_sums_by_currency[monnaie] += montant if item.type_payement != 'out' else -montant

            processed_data.append({
                'id': item.id,
                'date_payement': item.date_payement,
                'nom_offrande': str(item.nom_offrande),
                'num_compte': str(item.nom_offrande.num_compte),
                'type_payement': item.type_payement,
                'motif': item.motif,
                'type_monaie': monnaie,
                'montant': montant,
                'cumulative_sum': cumulative_sums_by_currency[monnaie],
            })

        return Response({'livre_caisse': processed_data}, status=200)


# =================== Rapport prevision =======================================

class RapportPrevisionAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAbonnementValide, IsSameChurch]

    def get(self, request):
        user_eglise = request.user.eglise  

        prevision_qs = Prevoir.objects.select_related('descript_prevision').filter(
            descript_prevision__user__eglise=user_eglise
        )

        grouped_previsions = prevision_qs.annotate(
            annee=ExtractYear('date_prevus')
        ).values(
            'descript_prevision__num_ordre',
            'descript_prevision__description_prevision',
            'annee'
        ).annotate(
            total_prevus=Coalesce(Sum('montant_prevus'), Decimal('0.00'), output_field=DecimalField())
        ).order_by('descript_prevision__num_ordre', 'annee')

        combined_data = []

        for group in grouped_previsions:
            num_ordre = group['descript_prevision__num_ordre']
            annee = group['annee']

            related_previsions = prevision_qs.filter(
                descript_prevision__num_ordre=num_ordre,
                date_prevus__year=annee
            ).values('nom_prevision', 'num_compte', 'montant_prevus')

            prevision_list = []

            for item in related_previsions:
                prevision_list.append({
                    'libelle': item['nom_prevision'],
                    'num_compte': item['num_compte'],
                    'prevision': item['montant_prevus'],
                })

            combined_data.append({
                'num_ordre': num_ordre,
                'description_prevision': group['descript_prevision__description_prevision'],
                'annee_prevus': annee,
                'total_prevus': group['total_prevus'],
                'lignes': prevision_list
            })

        return Response({'rapport_prevision': combined_data}, status=status.HTTP_200_OK)
