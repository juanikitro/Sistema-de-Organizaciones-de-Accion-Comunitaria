from django import forms
from organizations.models import Org

class SignForm(forms.ModelForm):
        class Meta:
            model = Org
            fields = (
                'doc',
                )
            widgets = {
                'doc': forms.FileInput(attrs={'class': 'form-control', 'required': 'True'})}
        
        def __init__(self, *args, **kwargs):
            super(SignForm, self).__init__(*args, **kwargs)
            self.fields['doc'].label = "Documentacion firmada:"