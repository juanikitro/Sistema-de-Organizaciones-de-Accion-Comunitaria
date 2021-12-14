# Python
from datetime import date, timedelta

# Django
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.db import IntegrityError
from django import forms
from django.shortcuts import render, redirect

# Models
from organizations.models import Org
from organizations.forms import DocumentForm

# Open Py XL (Para el excel)
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, Side, PatternFill
from django.http.response import HttpResponse

@login_required
def push_soac_view(request):
    values = {}
    if request.method == 'POST':
        name = request.POST['name']
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
        org.email = request.POST['email']
        org.mobile = request.POST['mobile']
        org.created = date.today()
        org.modified = date.today()
        # org.expiration = date.today() + timedelta(days=730)
        # org.renoved = date.today()
        org.state = 'no-registrada'

        if Org.objects.filter(name=name).first(): 
            return render(request, 'orgs/soac.html', {'error': 'Ya existe una organización con ese nombre, asegurate de no crear la misma', 'values': values})

        org.save()
        
        return render(request, 'orgs/soac.html', {'alert': 'Organización creada con exito', 'values': values})

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
        roac = request.POST.get('roac', False)

        if igj == '1':
            igj = '1'
        elif igj == '2':
            igj = '0'
        elif igj == 'nn':
            igj = ''
        elif igj == '0':
            igj = ''

        if roac == 'on':
            roac = 1
        elif roac == False:
            roac = 0

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
        print(roac)
        org = Org.objects.filter(name__startswith=name, domain__startswith=domain, address__contains=address, nhood__startswith=nhood, commune__contains=commune, areas__startswith=areas, igj__startswith=igj, type__startswith=type, public__startswith=public, postal_code__startswith=postal_code, roac__startswith=roac )

    return render(request, 'orgs/orgs.html', {'org': org, 'values': values})

class Excel_report(TemplateView):
    def get(self, *args, **kwargs):
        today = date.today()

        wb = Workbook()
        ws = wb.active
        ws['A1'] = f'Reporte de organizaciónes del dia: {today}'
        ws['A1'].alignment = Alignment(horizontal = 'center')
        ws['A1'].border = Border(left = Side(border_style = 'thin'), right = Side(border_style = 'thin'), bottom = Side(border_style = 'thin'), top = Side(border_style = 'thin'))
        ws['A1'].font = Font(name = 'Arial', size = 12)
        ws['A1'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')

        ws.merge_cells('A1:N1')

        ws['A3'] = 'id de org.'
        ws['A3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['B3'] = 'Nombre'
        ws['B3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['C3'] = 'Dominio'
        ws['C3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['D3'] = 'Direccion'
        ws['D3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['E3'] = 'Departamento'
        ws['E3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['F3'] = 'Barrio'
        ws['F3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['G3'] = 'Comuna'
        ws['G3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['H3'] = 'Areas'
        ws['H3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['I3'] = 'IGJ'
        ws['I3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['J3'] = 'Tipo'
        ws['J3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['K3'] = 'Publico'
        ws['K3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['L3'] = 'CP'
        ws['L3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['M3'] = 'Contacto'
        ws['M3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['N3'] = 'ROAC'
        ws['N3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')

        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 20
        ws.column_dimensions['D'].width = 20
        ws.column_dimensions['E'].width = 20
        ws.column_dimensions['F'].width = 20
        ws.column_dimensions['G'].width = 20
        ws.column_dimensions['H'].width = 20
        ws.column_dimensions['I'].width = 20
        ws.column_dimensions['J'].width = 20
        ws.column_dimensions['K'].width = 20
        ws.column_dimensions['L'].width = 20
        ws.column_dimensions['M'].width = 20

        cont = 4
        for u in org:
            ws.cell(row = cont, column = 1).value = u.id
            ws.cell(row = cont, column = 2).value = u.name
            ws.cell(row = cont, column = 3).value = u.domain
            ws.cell(row = cont, column = 4).value = u.address
            ws.cell(row = cont, column = 5).value = u.dpto
            ws.cell(row = cont, column = 6).value = u.nhood
            ws.cell(row = cont, column = 7).value = u.commune
            ws.cell(row = cont, column = 8).value = u.areas
            ws.cell(row = cont, column = 9).value = u.igj
            ws.cell(row = cont, column = 10).value = u.type
            ws.cell(row = cont, column = 11).value = u.public
            ws.cell(row = cont, column = 12).value = u.postal_code
            ws.cell(row = cont, column = 13).value = u.mobile
            ws.cell(row = cont, column = 14).value = u.roac
            cont += 1

        excel_name = f'Reporte de orgs. {today}.xlsx'
        response = HttpResponse(content_type = 'application/ms-excel')
        content = 'attachment; filename = {0}'.format(excel_name)
        response['Content-Disposition'] = content
        wb.save(response)
        return response

@login_required
def  register_roac_view(request, pk):
    selected_org = Org.objects.get(id=pk)

    info = {
        'id': selected_org.id,
        'name': selected_org.name,
    }

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance = selected_org)

        if form.is_valid():
            selected_org.state = 'pre-activa'
            form.save()
            return redirect('org', selected_org.id)
            
    else:
        form = DocumentForm()

    return render(request, 'orgs/register_org.html', {'pk': pk, 'info': info, 'form': form})

@login_required
def org_view(request, pk):
    org = Org.objects.get(id=pk)

    id = org.id
    name = org.name
    type = org.type
    public = org.public
    areas = org.areas
    address = org.address
    dpto = org.dpto
    postal_code = org.postal_code
    nhood = org.nhood
    commune = org.commune
    domain = org.domain
    email = org.email
    mobile = org.mobile
    state = org.state
    created = org.created
    renoved = org.renoved
    expiration = org.expiration
    modified = org.modified
    roac = org.roac
    doc = org.doc
    
    context = {
    'org':org,
    'id':id,
    'name':name,
    'type':type,
    'public':public,
    'areas':areas,
    'domain':domain,
    'commune':commune,
    'nhood':nhood,
    'postal_code':postal_code,
    'dpto':dpto,
    'address':address,
    'email':email,
    'mobile':mobile,
    'state':state,
    'created':created,
    'renoved':renoved,
    'expiration':expiration,
    'modified':modified,
    'roac': roac,
    'doc': doc,
    }

    return render(request, 'orgs/org.html', context)

login_required
def delete_org_view(request, pk):
    selected_org = Org.objects.get(id=pk)
    selected_org.delete()

    return redirect('orgs')

@login_required
def modify_org_view(request, pk):
    selected_org = Org.objects.get(id=pk)
    old_info = {
        'id': selected_org.id,
        'name': selected_org.name,
        'address': selected_org.address,
        'dpto': selected_org.dpto,
        'nhood': selected_org.nhood,
        'commune': selected_org.commune,
        'areas': selected_org.areas,
        'type': selected_org.type,
        'igj': selected_org.igj,
        'email': selected_org.email,
        'mobile': selected_org.mobile,
        'public': selected_org.public,
        'postal_code': selected_org.postal_code,
        'domain': selected_org.domain,
    }

    if request.method == 'POST':

        selected_org.name = request.POST['name']    
        selected_org.address = request.POST['address']    
        selected_org.dpto = request.POST['dpto']    
        selected_org.nhood = request.POST['nhood']    
        selected_org.commune = request.POST['commune']    
        selected_org.areas = request.POST['areas']    
        selected_org.type = request.POST['type']    
        selected_org.igj = request.POST['igj']    
        selected_org.email = request.POST['email']    
        selected_org.mobile = request.POST['mobile']    
        selected_org.public = request.POST['public']    
        selected_org.postal_code = request.POST['postal_code']    
        selected_org.domain = request.POST['domain']    
        selected_org.modified = date.today()

        try:
            selected_org.save()
        except IntegrityError:
            return render(request, 'orgs/modify_org.html', {'old': old_info, 'error': 'Ese nombre ya esta en uso'})
            
        return redirect('orgs')

    return render(request, 'orgs/modify_org.html', {'old': old_info})

@login_required
def down_org_view(request, pk):
    selected_org = Org.objects.get(id=pk)

    selected_org.roac = 0
    selected_org.state = 'no-registrada'

    try:
        selected_org.save()
    except IntegrityError:
        return redirect('org', selected_org.id)

    return redirect('org', selected_org.id)

@login_required
def download_org_view(request, pk):
    selected_org = Org.objects.get(id=pk)

    today = date.today()
    wb = Workbook()
    ws = wb.active
    ws['A1'] = f'Reporte de {selected_org.name} del dia: {today}'
    ws['A1'].alignment = Alignment(horizontal = 'center')
    ws['A1'].border = Border(left = Side(border_style = 'thin'), right = Side(border_style = 'thin'), bottom = Side(border_style = 'thin'), top = Side(border_style = 'thin'))
    ws['A1'].font = Font(name = 'Arial', size = 12)
    ws['A1'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')

    ws.merge_cells('A1:N1')

    ws['A3'] = 'id de org.'
    ws['A3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['B3'] = 'Nombre'
    ws['B3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['C3'] = 'Dominio'
    ws['C3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['D3'] = 'Direccion'
    ws['D3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['E3'] = 'Departamento'
    ws['E3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['F3'] = 'Barrio'
    ws['F3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['G3'] = 'Comuna'
    ws['G3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['H3'] = 'Areas'
    ws['H3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['I3'] = 'IGJ'
    ws['I3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['J3'] = 'Tipo'
    ws['J3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['K3'] = 'Publico'
    ws['K3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['L3'] = 'CP'
    ws['L3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['M3'] = 'Contacto'
    ws['M3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
    ws['N3'] = 'ROAC'
    ws['N3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')

    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 20
    ws.column_dimensions['F'].width = 20
    ws.column_dimensions['G'].width = 20
    ws.column_dimensions['H'].width = 20
    ws.column_dimensions['I'].width = 20
    ws.column_dimensions['J'].width = 20
    ws.column_dimensions['K'].width = 20
    ws.column_dimensions['L'].width = 20
    ws.column_dimensions['M'].width = 20

    cont = 4
    if selected_org:
        ws.cell(row = cont, column = 1).value = selected_org.id
        ws.cell(row = cont, column = 2).value = selected_org.name
        ws.cell(row = cont, column = 3).value = selected_org.domain
        ws.cell(row = cont, column = 4).value = selected_org.address
        ws.cell(row = cont, column = 5).value = selected_org.dpto
        ws.cell(row = cont, column = 6).value = selected_org.nhood
        ws.cell(row = cont, column = 7).value = selected_org.commune
        ws.cell(row = cont, column = 8).value = selected_org.areas
        ws.cell(row = cont, column = 9).value = selected_org.igj
        ws.cell(row = cont, column = 10).value = selected_org.type
        ws.cell(row = cont, column = 11).value = selected_org.public
        ws.cell(row = cont, column = 12).value = selected_org.postal_code
        ws.cell(row = cont, column = 13).value = selected_org.mobile
        ws.cell(row = cont, column = 14).value = selected_org.roac
        cont += 1

    excel_name = f'Reporte de {selected_org.name} {today}.xlsx'
    response = HttpResponse(content_type = 'application/ms-excel')
    content = 'attachment; filename = {0}'.format(excel_name)
    response['Content-Disposition'] = content
    wb.save(response)
    return response