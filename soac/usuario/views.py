# Django
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        cuit = request.POST['cuit']
        password = request.POST['password']
        user = authenticate(request, username=cuit, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'usuarios/login.html', {'error': 'Invalid username and password'})

    return render(request, 'usuarios/login.html')