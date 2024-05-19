from django import forms
from .models import Annonce

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['title','description']  # Ajoutez les champs supplémentaires si nécessaire
class SearchForm(forms.Form):
    q = forms.CharField(label='Recherche', max_length=100)