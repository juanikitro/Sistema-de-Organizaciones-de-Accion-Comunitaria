# Django
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import *

# Views
from home import views as home_views
from users import views as users_views
from organizations import views as organizations_views

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
    path('users/profile/<str:pk>/modify/', users_views.modify_profile_view, name='modify_profile'),
    path('users/profile/<str:pk>/reset/', users_views.reset_password_view, name='reset_password'),
    path('send_reset/', users_views.send_reset_password_view, name='send_reset_password'),
    path('send_reset/sended/<str:pk>/', users_views.reset_password_user_view, name='reset_password_user'),
    # Organizaciones
    path('organizations/soac', organizations_views.soac_view, name='soac'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)