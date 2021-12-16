from django import forms
from users.models import Profile
from organizations.models import Org

class SendToUsers(forms.Form):
    OPTIONS = ()
    for u in Profile.objects.all():
        tuple = ((u.id, f'{u.first_name} {u.last_name}'),)
        OPTIONS = OPTIONS + tuple

    users = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple
        (attrs={'class': 'text-light mb-3 no-bullet'}),
        choices=OPTIONS
        )

    def __init__(self, *args, **kwargs):
        super(SendToUsers, self).__init__(*args, **kwargs)
        self.fields['users'].label = "Usuarios destinatarios:"

class SendToOrgs(forms.Form):
    OPTIONS = ()
    for u in Org.objects.all():
        tuple = ((u.id, u.name),)
        OPTIONS = OPTIONS + tuple

    orgs = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple
        (attrs={'class': 'text-light mb-3 no-bullet'}),
        choices=OPTIONS
        )

    def __init__(self, *args, **kwargs):
        super(SendToOrgs, self).__init__(*args, **kwargs)
        self.fields['orgs'].label = "Organizaciones destinatarias:"