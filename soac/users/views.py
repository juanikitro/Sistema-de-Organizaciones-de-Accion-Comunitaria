# Python
from datetime import date 

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.transaction import atomic
from django.views.generic import TemplateView

# Models
from django.contrib.auth.models import User
from users.models import Profile

#Open Py XL
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, Side, PatternFill
from django.http.response import HttpResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password', False);
        print(username, password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Error en el cuit o la contraseña. Intente devuelta por favor.'})

    return render(request, 'users/login.html')

@login_required
@atomic
def signup_view(request):
    values = {}
    if request.method == 'POST':
        username = request.POST['username']        
        password = request.POST['password']
        email = request.POST['email']


        if User.objects.filter(username=username).first(): 
            return render(request, 'users/signup.html', {'error': 'El cuit ya pertenece a una cuenta'})
        if User.objects.filter(email=email).first(): 
            return render(request, 'users/signup.html', {'error': 'El email ya pertenece a una cuenta'})

        user = User.objects.create_user(username, email, password)
        user.username = username
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()

        profile = Profile()
        profile.user = user
        profile.email = email
        profile.username = username
        profile.first_name = request.POST['first_name']
        profile.last_name = request.POST['last_name']
        profile.level = request.POST['level']
        profile.mobile = request.POST['mobile']
        profile.save()

        values={
            'name': request.POST['first_name'],
            'lastname': request.POST['last_name'],
            'cuit': username,
            'email': email,
            'mobile': request.POST['mobile'],
        }
        
        return render(request, 'users/signup.html', {'alert': 'Usuario creado con exito! :)'})

    return render(request, 'users/signup.html', {'values': values})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def users_view(request):
    global profile
    profile = Profile.objects.all()
    values = {}
    if request.method == 'POST':
        name = request.POST.get('name', False)
        lastname = request.POST.get('lastname', False)
        cuit = request.POST.get('cuit', False)
        email = request.POST.get('email', False)
        mobile = request.POST.get('mobile', False)
        level = request.POST.get('level', False)

        if level == '1':
            level = 'comunal'
        elif level == '2':
            level = 'central'
        elif level == '3':
            level = 'presi'
        elif level == '4':
            level = 'admin'
        elif level == '0':
            level = ''

        values={
            'name': name,
            'lastname': lastname,
            'cuit': cuit,
            'email': email,
            'mobile': mobile,
        }
        profile = Profile.objects.filter(first_name__startswith=name, last_name__startswith=lastname, username__startswith=cuit, email__startswith=email, mobile__startswith=mobile, level__startswith=level)

    return render(request, 'users/users.html', {'profile': profile, 'values': values})

class Excel_report(TemplateView):
    def get(self, *args, **kwargs):
        today = date.today()

        wb = Workbook()
        ws = wb.active
        ws['A1'] = f'Reporte de usuarios del dia: {today}'
        ws['A1'].alignment = Alignment(horizontal = 'center')
        ws['A1'].border = Border(left = Side(border_style = 'thin'), right = Side(border_style = 'thin'), bottom = Side(border_style = 'thin'), top = Side(border_style = 'thin'))
        ws['A1'].font = Font(name = 'Arial', size = 12)
        ws['A1'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')

        ws.merge_cells('A1:G1')

        ws['A3'] = 'id de usuario'
        ws['A3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['B3'] = 'Cuit'
        ws['B3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['C3'] = 'Nombre'
        ws['C3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['D3'] = 'Apellido'
        ws['D3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['E3'] = 'Email'
        ws['E3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['F3'] = 'Contacto'
        ws['F3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')
        ws['G3'] = 'Nivel'
        ws['G3'].fill = PatternFill(start_color = 'ffc107', end_color = 'f3b600', fill_type='solid')

        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 20
        ws.column_dimensions['D'].width = 20
        ws.column_dimensions['E'].width = 20
        ws.column_dimensions['F'].width = 20
        ws.column_dimensions['G'].width = 20

        cont = 4
        for u in profile:
            ws.cell(row = cont, column = 1).value = u.id
            ws.cell(row = cont, column = 2).value = u.username
            ws.cell(row = cont, column = 3).value = u.first_name
            ws.cell(row = cont, column = 4).value = u.last_name
            ws.cell(row = cont, column = 5).value = u.email
            ws.cell(row = cont, column = 6).value = u.mobile
            ws.cell(row = cont, column = 7).value = u.level
            cont += 1

        excel_name = f'Reporte de usuarios {today}.xlsx'
        response = HttpResponse(content_type = 'application/ms-excel')
        content = 'attachment; filename = {0}'.format(excel_name)
        response['Content-Disposition'] = content
        wb.save(response)
        return response

@login_required
def profile_view(request, pk):
    profile = Profile.objects.get(id=pk)
    user = User.objects.get(id=profile.user_id)

    id = profile.id
    username = user.username
    name = user.first_name + ' ' + user.last_name
    email = user.email
    mobile = profile.mobile
    created = profile.created
    modified = profile.modified
    level = ''
    if profile.level == 'admin':
        level = 'Administrador de ROAC'
    elif profile.level == 'presidente':
        level = 'Presidente'
    elif profile.level == 'central':
        level = 'Usuario de sede central'
    elif profile.level == 'comunal':
        level = 'Usuario de sede comunal'
    state = ''
    if user.is_active == True:
        state = 'Activo'
    else:
        state = 'Inactivo'
    context = {'profile':profile,
    'id':id,
    'username':username,
    'name':name,
    'email':email,
    'mobile':mobile,
    'modified':modified,
    'created':created,
    'active':state,
    'level':level}
    return render(request, 'users/profile.html', context)

@login_required
def delete_profile_view(request, pk):
    selected_profile = Profile.objects.get(id=pk)
    selected_user = User.objects.get(id=selected_profile.user_id)

    selected_profile.delete()
    selected_user.delete()

    profile = Profile.objects.all()
    return render(request, 'users/users.html', {'profile': profile})