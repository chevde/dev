from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Annonce, UploadImage
from .serializers import AnnonceSerializer, UploadImageSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from .forms import UploadImageForm
from django.contrib.auth import authenticate, login
# API views
@api_view(['GET'])
def search_annonce(request):
    query = request.GET.get('key')
    annonces = Annonce.objects.filter(title__icontains=query)
    serializer = AnnonceSerializer(annonces, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_annonce(request):
    serializer = AnnonceSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_announces(request):
    annonces = Annonce.objects.all()
    serializer = AnnonceSerializer(annonces, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_annonce(request, annonce_id):
    try:
        annonce = Annonce.objects.get(pk=annonce_id)
    except Annonce.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    annonce.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def update_annonce(request, pk):
    try:
        annonce = Annonce.objects.get(pk=pk)
    except Annonce.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AnnonceSerializer(annonce, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()

        # Handle image updates
        images_data = request.FILES.getlist('images')
        if images_data:
            # Delete old images
            UploadImage.objects.filter(annonce=annonce).delete()
            # Add new images
            for image_data in images_data:
                UploadImage.objects.create(annonce=annonce, image=image_data)

        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

# Views for HTML rendering (if needed)
@login_required(login_url='login')
def upload_photo(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Créer une nouvelle annonce
            annonce = Annonce.objects.create(
                user = request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description']
            )
            # Enregistrer les images associées à l'annonce
            files = request.FILES.getlist('image')
            for file in files:
                UploadImage.objects.create(
                    annonce=annonce,
                    image=file
                )
            return redirect('photo_list')
    else:
        form = UploadImageForm()
    return render(request, 'upload_image.html', {'form': form})

@login_required(login_url='login')
def photo_list(request):
    annonces = Annonce.objects.filter(user=request.user)
    return render(request, 'show_files.html', {'annonces': annonces})
def home(request):
    annonces = Annonce.objects.all()
    return render(request, 'index.html', {'annonces': annonces})

@login_required
def user_announces(request):
    # Récupérer les annonces de l'utilisateur connecté
    annonces = Annonce.objects.filter(user=request.user)
    return render(request, 'user_announces.html', {'annonces': annonces})

def delete_all_photos(request):
    UploadImage.objects.all().delete()
    return redirect('photo_list')

def delete_photo(request, photo_id):
    photo = UploadImage.objects.get(pk=photo_id)
    photo.delete()
    return redirect('photo_list')
def delete_annonce(request, annonce_id):
    annonce = Annonce.objects.get( pk=annonce_id)
    annonce.delete()
    return redirect('photo_list')


def search(request):
    query = request.GET.get('q')
    annonces = Annonce.objects.filter(title__icontains=query)  # Filtrez les annonces par titre
    return render(request, 'index.html', {'annonces': annonces})

@login_required(login_url='login')
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

# views.py

class CustomLoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        # Récupérer les données du formulaire
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Authentifier l'utilisateur
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            # Si l'utilisateur existe et les informations d'identification sont correctes, connectez-vous
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            # Si l'authentification échoue, redirigez l'utilisateur vers la page de connexion
            return HttpResponseRedirect(reverse('login'))

    def get_success_url(self):
        # Rediriger l'utilisateur vers votre chemin de profil après la connexion réussie
        return reverse('home')
    
def CustomLogoutView(request):
    logout(request)
    return redirect('home')  


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirection vers l'URL souhaité après le signup
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})