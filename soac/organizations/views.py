# Python
from datetime import date 

# Django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import IntegrityError

# Models
from django.contrib.auth.models import User
from organizations.models import Org
@login_required
def soac_view(request):
    values = {}
    if request.method == 'POST':
        name = request.POST['name']

        if Org.objects.filter(name=name).first(): 
            return render(request, 'users/signup.html', {'error': 'Ya existe una organizacion con ese nombre, asegurate de no crear la misma!'})

        org = Org()
        org.name = name
        org.domain = request.POST['domain']
        org.address = request.POST['address']
        org.dpto = request.POST['dpto']
        org.nhood = request.POST['nhood']
        org.commune = request.POST['commune']
        org.areas = request.POST['areas']
        org.igj = request.POST['igj']
        org.type = request.POST['type']
        org.public = request.POST['public']
        org.postal_code = request.POST['postal_code']
        org.created = date.today()
        org.modified = date.today()
        # for ROAC
        # org.roac = request.POST['roac']
        # org.nota_solicitud_inscripcion = request.POST['nota_solicitud_inscripcion']
        # org.acta_libro_actas = request.FILES['acta_libro_actas']
        # org.acta_asamblea = request.FILES['acta_asamblea']
        # org.estatuto_social = request.FILES['estatuto_social']
        # org.nomina_comision = request.FILES['nomina_comision']
        # org.dni_comision = request.FILES['dni_comision']
        # org.nomina_asociados = request.FILES['nomina_asociados']
        # org.sede_social = request.FILES['sede_social']
        # org.abl = request.FILES['abl']
        # org.extra = request.FILES['extra']
        org.save()

        values={
            'org.name': name,
            'org.address': request.POST['address'],
            'org.dpto': request.POST['dpto'],
            'org.nhood': request.POST['nhood'],
            'org.commune': request.POST['commune'],
            'org.areas': request.POST['areas'],
            'org.igj': request.POST['igj'],
            'org.public': request.POST['public'],
            'org.postal_code': request.POST['postal_code'],
            'org.domain': request.POST['domain'],
        }
        return render(request, 'orgs/soac.html', {'alert': 'Organizacion creada con exito'})

    return render(request, 'orgs/soac.html', {'values': values})