# Python
from datetime import date 

# Django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Models
from organizations.models import Org
@login_required
def push_soac_view(request):
    values = {}
    if request.method == 'POST':
        name = request.POST['name']

        if Org.objects.filter(name=name).first(): 
            return render(request, 'orgs/soac.html', {'error': 'Ya existe una organizacion con ese nombre, asegurate de no crear la misma'})

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

        return render(request, 'orgs/soac.html', {'alert': 'Organizacion creada con exito', 'values': values})

    return render(request, 'orgs/soac.html', {'values': values})

@login_required
def orgs_view(request):
    global org
    org = Org.objects.all()
    values = {}
    if request.method == 'POST':
        name = request.POST.get('name', False)
        domain = request.POST.get('domain', False)
        address = request.POST.get('address', False)
        nhood = request.POST.get('nhood', False)
        commune = request.POST.get('commune', False)
        areas = request.POST.get('areas', False)
        igj = request.POST.get('igj', False)
        type = request.POST.get('type', False)
        public = request.POST.get('public', False)
        postal_code = request.POST.get('postal_code', False)
        
        if domain == '1':
            domain = 'propia'
        elif domain == '2':
            domain = 'alquilada'
        elif domain == 'nn':
            domain = 'nn'
        elif domain == '0':
            domain = ''

        if igj == '1':
            igj = '1'
        elif igj == '2':
            igj = '0'
        elif igj == 'nn':
            igj = ''
        elif igj == '0':
            igj = ''

        values={
            'name': name,
            'domain': domain,
            'address': address,
            'nhood': nhood,
            'commune': commune,
            'areas': areas,
            'igj': igj,
            'type': type,
            'public': public,
            'postal_code': postal_code,
        }

        org = Org.objects.filter(name__startswith=name, domain__startswith=domain, address__startswith=address, nhood__startswith=nhood, commune__startswith=commune, areas__startswith=areas, igj__startswith=igj, type__startswith=type, public__startswith=public, postal_code__startswith=postal_code )

    return render(request, 'orgs/orgs.html', {'org': org, 'values': values})