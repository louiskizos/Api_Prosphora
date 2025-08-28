from rest_framework import serializers

from .models import Payement_Offrande, Prevoir

# Sérialiseur pour Payement_Offrande
class PayementOffrandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payement_Offrande
        fields = ['nom_offrande', 'departement', 'montant', 'date_payement', 'annee']

# Sérialiseur pour Prevoir
class PrevoirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prevoir
        fields = ['descript_prevision', 'montant_prevus', 'annee_prevus']


from rest_framework import serializers
from .models import Church, Abonnement, User
from django.contrib.auth import authenticate

class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = '__all__'

class AbonnementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abonnement
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'nom', 'role', 'eglise']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            abonnement = Abonnement.objects.filter(eglise=user.eglise).order_by('-date').first()
            return {
                'user_id': user.id,
                'nom': user.nom,
                'email': user.email,
                'role': user.role,
                'eglise': user.eglise.nom,
                'abonnement_mois': abonnement.mois if abonnement else None,
                'abonnement_date': abonnement.date if abonnement else None,
            }
        raise serializers.ValidationError("Email ou mot de passe incorrect.")
