#Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

#Models
from organizations.models import Org

#Analisis
@login_required
def analysis_view(request):
    global preactivas
    preactivas = Org.objects.filter(state = 'pre-activa').order_by('-registration_request')
    nothing = preactivas.first()

    return render(request, 'inbox/analysis.html', {'preactivas': preactivas, 'nothing': nothing})

@login_required
def return_pre_view(request, pk):
    selected_org = Org.objects.get(id=pk)

    selected_org.state = 'editar'
    selected_org.doc = ''
    selected_org.save()

    return redirect('analysis')

@login_required
def sign_pre_view(request, pk):
    selected_org = Org.objects.get(id=pk)

    selected_org.state = 'firmar'
    selected_org.save()

    return redirect('analysis')

#Edicion
@login_required
def edit_view(request):
    global editar
    editar = Org.objects.filter(state = 'editar').order_by('-registration_request')
    nothing = editar.first()

    return render(request, 'inbox/edit.html', {'editar': editar, 'nothing': nothing})
    
#Sign
@login_required
def sign_view(request):
    global sign
    sign = Org.objects.filter(state = 'firmar').order_by('-registration_request')
    nothing = sign.first()

    return render(request, 'inbox/sign.html', {'sign': sign, 'nothing': nothing})

@login_required
def return_sign_view(request, pk):
    selected_org = Org.objects.get(id=pk)

    selected_org.state = 'pre-activa'
    selected_org.doc = ''
    selected_org.save()

    return redirect('sign')