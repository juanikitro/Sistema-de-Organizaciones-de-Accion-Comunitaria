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

    return render(request, 'users/signup.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def users_view(request):
    global profile
    profile = Profile.objects.all()
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

        profile = Profile.objects.filter(first_name__startswith=name, last_name__startswith=lastname, username__startswith=cuit, email__startswith=email, mobile__startswith=mobile, level__startswith=level)

    return render(request, 'users/users.html', {'profile': profile})

class Excel_report(TemplateView):
    def get(self, *args, **kwargs):
        wb = Workbook()
        ws = wb.active
        ws['A1'] = 'REPORTE DE USUARIOS'

        ws.merge_cells('A1:Z1')

        ws['A2'] = 'id'
        ws['B2'] = 'Cuit'
        ws['C2'] = 'Nombre'
        ws['D2'] = 'Apellido'
        ws['E2'] = 'Email'
        ws['F2'] = 'Contacto'
        ws['G2'] = 'Nivel'

        cont = 3

        for u in profile:
            ws.cell(row = cont, column = 1).value = u.id
            ws.cell(row = cont, column = 2).value = u.username
            ws.cell(row = cont, column = 3).value = u.first_name
            ws.cell(row = cont, column = 4).value = u.last_name
            ws.cell(row = cont, column = 5).value = u.email
            ws.cell(row = cont, column = 6).value = u.mobile
            ws.cell(row = cont, column = 7).value = u.level
            cont += 1

        excel_name = 'Reporte_de_usuarios.xlsx'
        response = HttpResponse(content_type = 'application/ms-excel')
        content = 'attachment; filename = {0}'.format(excel_name)
        response['Content-Disposition'] = content
        wb.save(response)
        return response

@login_required
def profile_view(request, pk):
    profile = Profile.objects.get(id=pk)
    user = User.objects.get(id=profile.user_id)

    username = user.username
    name = user.first_name + ' ' + user.last_name
    email = user.email
    mobile = profile.mobile
    created = profile.created
    modified = profile.modified
    level = ''
    if profile.level == 'admin':
        level = 'Administrador de SOAC'
    elif profile.level == 'presi':
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
     'username':username,
     'name':name,
     'email':email,
     'mobile':mobile,
     'modified':modified,
     'created':created,
     'active':state,
     'level':level}
    return render(request,
     'users/profile.html',
     context)