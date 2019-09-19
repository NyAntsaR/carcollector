from django.forms import ModelForm
from .models import Gas

class GasForm(ModelForm):
    class Meta:
        model = Gas
        fields = ['date', 'category']

form = GasForm()