from django import forms
from .models import Org

class DocumentForm(forms.ModelForm):
        class Meta:
            model = Org
            fields = (
                'certificate',
                )
            widgets = {
                'certificate': forms.FileInput(attrs={'class': 'form-control', 'required': 'True'})}
        
        def __init__(self, *args, **kwargs):
            super(DocumentForm, self).__init__(*args, **kwargs)
            self.fields['certificate'].label = ""