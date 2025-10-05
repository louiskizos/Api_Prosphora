from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone




# === Eglise ===
class Church(models.Model):
    nom = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    pasteur = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nom

# === Abonnement ===
class Abonnement(models.Model):
    eglise = models.ForeignKey(Church, on_delete=models.CASCADE, related_name='abonnements')
    mois = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.eglise.nom} - {self.mois} mois"

# === User Manager ===
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'utilisateur doit avoir un email.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# === Custom User ===
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('gestionnaire', 'Gestionnaire'),
        ('pasteur', 'Pasteur'),
        ('comptable', 'Comptable'),
        ('caissier', 'Caissier'),
    )

    eglise = models.ForeignKey(Church, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date = models.DateField(default=timezone.now)

    is_active = True
    is_staff = False

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'role', 'eglise']

    def __str__(self):
        return self.email



# === Groupe Offrandes ===
class Groupe_Offrandes(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_ordre = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description_recette = models.CharField(max_length=100)
    
    def __str__(self):
        return self.description_recette


# === Sorte Offrande ===
class Sorte_Offrande(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descript_recette = models.ForeignKey(Groupe_Offrandes, on_delete=models.CASCADE)
    num_compte = models.CharField(max_length=20)
    nom_offrande = models.TextField(max_length=50)
    
    def __str__(self):
        return self.nom_offrande

    

# === Payement ===
class Payement_Offrande(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom_offrande = models.ForeignKey(Sorte_Offrande, on_delete=models.CASCADE)
    departement = models.CharField(max_length=100)
    type_payement = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    montant_lettre = models.CharField(max_length=255)
    type_monaie = models.CharField(max_length=100, default="CDF")
    motif = models.CharField(max_length=255,)
    date_payement = models.DateField()
    annee = models.IntegerField()


# === Ahadi ===
class Ahadi(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom_offrande = models.ForeignKey(Sorte_Offrande, on_delete=models.CASCADE)
    nom_postnom = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    montant_lettre = models.CharField(max_length=255)
    motif = models.CharField(max_length=255)
    type_monaie = models.CharField(max_length=100, default="CDF")
    date_ahadi = models.DateField()
    annee = models.IntegerField()



# class dime(models.Model):
    
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     nom_offrande = models.ForeignKey(Sorte_Offrande, on_delete=models.CASCADE)
#     nom_postnom = models.CharField(max_length=100)
#     chapelle = models.CharField(max_length=100)
#     montant = models.DecimalField(max_digits=15, decimal_places=2)
#     montant_lettre = models.CharField(max_length=255)
#     motif = models.CharField(max_length=255)
#     date_ahadi = models.DateField()
#     annee = models.IntegerField()
  
    


# === Etat Besoin ===
class EtatBesoin(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.CharField(max_length=100)
    designation = models.CharField(max_length=255, default="Aucune désignation")
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_monaie = models.CharField(max_length=100, default="CDF")
    quantite = models.CharField(max_length=100)
    motif = models.TextField()
    date_etat_besoin = models.DateField(auto_now_add=True)
    validation_pasteur = models.BooleanField(default=False)
    #commentaire_pasteur = models.TextField()
    validation_caisse = models.BooleanField(default=False)

    def __str__(self):
        return self.service





# === Groupe Previsions ===
class Groupe_Previsions(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_ordre = models.CharField(max_length=100)
    description_prevision = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.num_ordre


# === Prevoir ===
class Prevoir(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descript_prevision = models.ForeignKey(Groupe_Previsions, on_delete=models.CASCADE)
    num_compte = models.BigIntegerField()
    nom_prevision = models.TextField(max_length=50)
    montant_prevus = models.DecimalField(max_digits=15, decimal_places=2)
    type_monaie = models.CharField(max_length=100, default="CDF")
    annee_prevus = models.IntegerField()
    def __str__(self):
        return self.nom_prevision
    
    
# class PayementOffrandeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payement_Offrande
#         fields = ['nom_offrande', 'departement', 'montant', 'date_payement', 'annee']
        
# class PrevoirSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Prevoir
#         fields = ['descript_prevision', 'montant_prevus', 'annee_prevus']