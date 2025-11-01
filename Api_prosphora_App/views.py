from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from .models import *
from rest_framework import generics, mixins
from .permissions import IsAbonnementValide, IsSameChurch
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Q, OuterRef, Subquery, Sum, DecimalField, BigIntegerField
from decimal import Decimal
from django.db.models.functions import Coalesce, ExtractYear, Cast



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

class LoginView(APIView):
    
    def post(self, request):

        num_phone = request.data.get("num_phone")
        password = request.data.get("password")
        print(f"Login attempt: num_phone={num_phone}, password={'*' * len(password) if password else None}")

        user = authenticate(request, num_phone=num_phone, password=password)

        if user is not None:
            login(request, user)

            
            dernier_abonnement = user.eglise.abonnements.order_by('-date').first()

            response_data = {
                "user_id": user.id,
                "nom": user.nom,
                "num_phone": user.num_phone,
                "role": user.role,
                "eglise": user.eglise.nom if user.eglise else None,
                "abonnement_mois": dernier_abonnement.mois if dernier_abonnement else None,
                "abonnement_date": dernier_abonnement.date if dernier_abonnement else None
            }

            return Response(response_data, status=status.HTTP_200_OK)

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

    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
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

    permission_classes = [IsAuthenticated]


    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Abonnement.objects.filter(pk=pk)
        return Abonnement.objects.all()
    
    # def get_queryset(self):
    #     abonnement_eglise = self.request.user.eglise
    #     pk = self.kwargs.get('pk')
    #     if pk:
    #         return Abonnement.objects.filter(pk=pk, id=abonnement_eglise.id)
        
    #     return Abonnement.objects.filter(id=abonnement_eglise.id)



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
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
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

    permission_classes = [IsAuthenticated]


    queryset = Groupe_Offrandes.objects.all()
    serializer_class = Groupe_OffrandesSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Groupe_Offrandes.objects.filter(pk=pk)
        return Groupe_Offrandes.objects.all()
    
    def get_queryset(self):
        user_eglise = self.request.user.eglise
        return Groupe_Offrandes.objects.filter(user__eglise=user_eglise)


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    
    def post(self, request):
        serializer = Groupe_OffrandesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Groupe d'offrande créé."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
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
    permission_classes = [IsAuthenticated, IsSameChurch]
    serializer_class = Sorte_OffrandeSerializer
    queryset = Sorte_Offrande.objects.all()
    lookup_field = 'pk'

    # def get_queryset(self):
        
    #     user_eglise = self.request.user.eglise
    #     pk = self.kwargs.get('pk')
    #     grp = self.kwargs.get('grp')

    #     queryset = Sorte_Offrande.objects.filter(descript_recette__user__eglise=user_eglise)

    #     if pk:
    #         queryset = queryset.filter(pk=pk)
    #     if grp:
    #         queryset = queryset.filter(descript_recette__id=grp)

    #     return queryset

    def get_queryset(self):
        
        user_eglise = self.request.user.eglise
        pk = self.kwargs.get('pk')
        grp = self.kwargs.get('grp')

        queryset = Sorte_Offrande.objects.filter(
            descript_recette__user__eglise=user_eglise
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

    def put(self, request, *args, **kwargs):
        
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Suppression d'une offrande.
        """
        return self.destroy(request, *args, **kwargs)
    
# ======================== GROUPE PREVISION =========================
class Groupe_Previsions_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):

    #permission_classes = [IsAuthenticated,]


    queryset = Groupe_Previsions.objects.all()
    serializer_class = Groupe_PrevisionsSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Groupe_Previsions.objects.filter(pk=pk)
        return Groupe_Previsions.objects.all()
    


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = Groupe_PrevisionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Groupe de prévision créé."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

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

    #permission_classes = [IsAuthenticated,]


    queryset = Prevoir.objects.all()
    serializer_class = PrevoirSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Prevoir.objects.filter(pk=pk)
        return Prevoir.objects.all()
    


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = PrevoirSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Prévoir créé."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)   
    


# ======================== PAYEMENT =========================

class Payement_Offrande_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):

    permission_classes = [IsAuthenticated, IsSameChurch]


    queryset = Payement_Offrande.objects.all()
    serializer_class = PayementOffrandeSerializer
    lookup_field = 'pk'
    
    def get_queryset(self):
        user_eglise = self.request.user.eglise
        pk = self.kwargs.get('pk')

        queryset = Payement_Offrande.objects.filter(
            nom_offrande__descript_recette__user__eglise=user_eglise
        )

        if pk:
            queryset = queryset.filter(pk=pk)

        return queryset


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = PayementOffrandeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Payement créé."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)   


# ======================== AHADI =========================

class Ahadi_Mixins(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = Ahadi.objects.all()
    serializer_class = AhadiSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsSameChurch]

    def get_queryset(self):
        
        user_eglise = self.request.user.eglise
        pk = self.kwargs.get('pk')

        queryset = Ahadi.objects.filter(
            nom_offrande__descript_recette__user__eglise=user_eglise
        )

        if pk:
            queryset = queryset.filter(pk=pk)

        return queryset

    def get(self, request, *args, **kwargs):
        
        engagements = self.get_queryset()

        paiements = (
            Payement_Offrande.objects.filter(
                type_payement="in",
                nom_offrande=OuterRef('nom_offrande'),
                departement=OuterRef('nom_postnom'),
                nom_offrande__descript_recette__description_recette="LES ENGAGEMENTS DES ADHERENTS",
                nom_offrande__descript_recette__user__eglise=request.user.eglise  # <-- filtre sécurité ajouté
            )
            .values('nom_offrande', 'departement')
            .annotate(total_paye=Sum('montant'))
            .values('total_paye')
        )

        engagements = engagements.annotate(
            total_paye=Subquery(paiements, output_field=models.DecimalField(max_digits=15, decimal_places=2))
        )

        for e in engagements:
            e.reste = (e.montant or Decimal('0')) - (e.total_paye or Decimal('0'))

        serializer = self.get_serializer(engagements, many=True)
        return Response({"ahadi_data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Ahadi créé avec succès.", "data": serializer.data},
                        status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        
        return self.update(request, *args, **kwargs)

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

    permission_classes = [IsAuthenticated, IsAbonnementValide]


    queryset = EtatBesoin.objects.all()
    serializer_class = EtatBesoinSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return EtatBesoin.objects.filter(pk=pk)
        return EtatBesoin.objects.all()
    


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = EtatBesoinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Etat de besoin créé."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)

# ======================== Rapport Bilan =========================   

class BilanAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        prevision_qs = Prevoir.objects.select_related('descript_prevision')
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

        paiement_qs = Payement_Offrande.objects.select_related('nom_offrande').annotate(
            annee_payement=ExtractYear('date_payement'),
            compte_rapprochement=Cast('nom_offrande__num_compte', output_field=BigIntegerField())
        )

        paiement_totals_by_currency = paiement_qs.values(
            'compte_rapprochement',
            'annee_payement',
            'type_monaie',
            'nom_offrande__nom_offrande'
        ).annotate(
            total_recette=Coalesce(
                Sum('montant', filter=Q(type_payement='in')),
                Decimal('0.00'),
                output_field=DecimalField()
            ),
            total_depense=Coalesce(
                Sum('montant', filter=Q(type_payement='out')),
                Decimal('0.00'),
                output_field=DecimalField()
            ),
        )

        payments_dict = {}
        for item in paiement_totals_by_currency:
            key = (item['compte_rapprochement'], item['annee_payement'])
            if key not in payments_dict:
                payments_dict[key] = {
                    'libelle': item['nom_offrande__nom_offrande'],
                    'par_devise': {}
                }
            devise = item['type_monaie']
            payments_dict[key]['par_devise'][devise] = {
                'recette': item['total_recette'],
                'depense': item['total_depense']
            }

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
                key = (compte, annee)
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

            def format_totals(total_dict):
                return {devise: montant for devise, montant in total_dict.items() if montant > 0}

            combined_data.append({
                'num_ordre': num_ordre,
                'description_prevision': group['descript_prevision__description_prevision'],
                'annee_prevus': annee,
                'total_prevus': group['total_prevus'],
                'total_recettes_par_devise': format_totals(current_totals['recettes']),
                'total_depenses_par_devise': format_totals(current_totals['depenses']),
                'lignes': prevision_list + paiement_list
            })

        return Response({'bilan_data': combined_data}, status=status.HTTP_200_OK)
    
# =================== Rapport livre de caisse =======================================



class LivreCaisseAPIView(APIView):
    
    permission_classes = [IsAuthenticated, IsAbonnementValide, IsSameChurch]

    def get(self, request):
        user_eglise = request.user.eglise  

        data_queryset = Payement_Offrande.objects.filter(
            nom_offrande__descript_recette__user__eglise=user_eglise
        ).order_by('type_monaie', 'date_payement')

        cumulative_sums_by_currency = {}
        processed_data = []

        for item in data_queryset:
            monnaie = item.type_monaie
            montant = item.montant or 0

            # Initialise la devise si pas encore vue
            if monnaie not in cumulative_sums_by_currency:
                cumulative_sums_by_currency[monnaie] = 0

            # Ajuste le cumul selon le type de paiement
            if item.type_payement == 'out':
                cumulative_sums_by_currency[monnaie] -= montant
            else:
                cumulative_sums_by_currency[monnaie] += montant

            processed_data.append({
                'id': item.id,
                'date_payement': item.date_payement,
                'nom_offrande': str(item.nom_offrande),
                'num_compte': str(item.nom_offrande.num_compte),
                'type_payement': item.type_payement,
                'type_monaie': monnaie,
                'montant': montant,
                'cumulative_sum': cumulative_sums_by_currency[monnaie],
            })

        return Response({'livre_caisse': processed_data}, status=status.HTTP_200_OK)


# =================== Rapport prevision =======================================
