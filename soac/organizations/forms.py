from django import forms
from .models import Org

class DocumentForm(forms.ModelForm):
        class Meta:
            model = Org
            fields = (
                'doc',
                )
            widgets = {
                'doc': forms.FileInput(attrs={'class': 'form-control', 'required': 'True'})}