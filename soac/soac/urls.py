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
    path('users/', users_views.users_view, name='users'),
    path('users/user_report', users_views.Excel_report.as_view(), name='user_report'),
    path('users/profile/<str:pk>/', users_views.profile_view, name='profile'),
    path('users/profile/<str:pk>/delete/', users_views.delete_profile_view, name='delete_profile'),
]
