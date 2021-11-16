# Django
from django.contrib import admin
from django.urls import path

# Views
from home import views as home_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #Home
    path('', home_views.home_view, name='home'),

    #Usuarios
    path('signup/', users_views.signup_view, name='signup'),
    path('logout/', users_views.logout_view, name='logout'),
    path('login/', users_views.login_view, name='login'),
    path('profile/<str:pk_test>/', users_views.profile_view, name='profile'),

]
