# Django
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import *

# Views
from home import views as home_views
from users import views as users_views
from organizations import views as organizations_views
from inbox import views as inbox_views

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

    #Organizaciones
    path('organizations/', organizations_views.orgs_view, name='orgs'),
    path('organizations/orgs_report', organizations_views.Excel_report.as_view(), name='orgs_report'),
    path('organizations/soac', organizations_views.push_soac_view, name='soac'),
    path('organizations/roac', organizations_views.push_roac_view, name='roac'),
    path('organizations/org/<str:pk>/', organizations_views.org_view, name='org'),   
    path('organizations/org/<str:pk>/delete/', organizations_views.delete_org_view, name='delete_org'),
    path('organizations/org/<str:pk>/down/', organizations_views.down_org_view, name='down_org'),
    path('organizations/org/<str:pk>/register/', organizations_views.register_request_view, name='register_roac'),
    path('organizations/org/<str:pk>/modify/', organizations_views.modify_org_view, name='modify_org'),
    path('organizations/org/<str:pk>/org_report/', organizations_views.download_org_view, name='org_report'),

    #Bandejas
    path('inbox/analysis', inbox_views.analysis_view, name='analysis'),
    path('inbox/analysis/return/<str:pk>/', inbox_views.return_pre_view, name='return_pre'),
    path('inbox/analysis/sign/<str:pk>/', inbox_views.sign_pre_view, name='sign_pre'),
    path('inbox/edit', inbox_views.edit_view, name='edit'),
    path('organizations/org/<str:pk>/noregister/', organizations_views.noregister_org_view, name='noregister_org'),
    path('inbox/sign', inbox_views.sign_view, name='sign'),
    path('inbox/sign/return/<str:pk>/', inbox_views.return_sign_view, name='return_sign'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)