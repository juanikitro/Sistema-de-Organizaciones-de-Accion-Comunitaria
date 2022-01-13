#Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

#Models
from organizations.models import Org
from users.models import Profile

#Forms
from inbox.forms import SignForm

#Analisis
@login_required
def analysis_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    global preactivas
    preactivas = Org.objects.filter(state = 'pre-activa').order_by('-registration_request')
    nothing = preactivas.first()

    return render(request, 'inbox/analysis.html', {'preactivas': preactivas, 'nothing': nothing, 'level': profile_level})

@login_required
def return_pre_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    selected_org = Org.objects.get(id=pk)
    if request.method == 'POST':
        selected_org.state = 'editar'
        selected_org.doc = ''
        selected_org.msg = request.POST.get('msg')
        selected_org.save()
        return redirect('analysis') 

    return render(request, 'inbox/return_pre.html', {'org': selected_org, 'level': profile_level})

@login_required
def sign_pre_view(request, pk):
    selected_org = Org.objects.get(id=pk)

    selected_org.state = 'firmar'
    selected_org.save()

    return redirect('analysis')

#Edicion
@login_required
def edit_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    global editar
    editar = Org.objects.filter(state = 'editar').order_by('-registration_request')
    nothing = editar.first()

    return render(request, 'inbox/edit.html', {'editar': editar, 'nothing': nothing, 'level': profile_level})
    
#Firma
@login_required
def sign_view(request):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level

    global sign
    sign = Org.objects.filter(state = 'firmar').order_by('-registration_request')
    nothing = sign.first()

    return render(request, 'inbox/sign.html', {'sign': sign, 'nothing': nothing, 'level': profile_level})

@login_required
def return_sign_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level
    
    selected_org = Org.objects.get(id=pk)
    if request.method == 'POST':
        selected_org.state = 'pre-activa'
        selected_org.msg = request.POST.get('msg')
        selected_org.save()
        return redirect('sign') 

    return render(request, 'inbox/return_sign.html', {'org': selected_org, 'level': profile_level})

def signing_view(request, pk):
    user_id = request.user.id
    profile_level = Profile.objects.get(user_id = user_id).level
    
    selected_org = Org.objects.get(id=pk)
    if request.method == 'POST':
        form = SignForm(request.POST, request.FILES, instance = selected_org)

        if form.is_valid():
            selected_org.state = 'activa'
            selected_org.roac = 'Si'
            selected_org.enrolled = datetime.now().date()
            selected_org.save()
            form.save()
            return redirect('org', selected_org.id)

    else:
        form = SignForm()

    return render(request, 'inbox/signing.html', {'org': selected_org, 'form': form, 'level': profile_level})