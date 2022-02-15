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
from comunications import views as comunications_views
from events import views as events_views
from activities import views as activities_views
from visits import views as visits_views
from history import views as history_views
from claims import views as claims_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #Home
    path('', home_views.home_view, name='home'),

    #Usuarios
    path('signup/', users_views.signup_view, name='signup'),
    path('signup_comunal/', users_views.signup_comunal_view, name='signup_comunal'),
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
    path('organizations/org/<str:pk>/msgregister/', inbox_views.msgregister_request_view, name='msgregister_roac'),
    path('organizations/org/<str:pk>/register/', organizations_views.register_request_view, name='register_roac'),
    path('organizations/org/<str:pk>/modify/', organizations_views.modify_org_view, name='modify_org'),
    path('organizations/org/<str:pk>/org_report/', organizations_views.download_org_view, name='org_report'),
    path('organizations/org/<str:pk>/org_pdf/', organizations_views.PdfExport.as_view(), name='org_report_pdf'),

    #Bandejas
    path('inbox/analysis', inbox_views.analysis_view, name='analysis'),
    path('inbox/forexpire', inbox_views.forexpire_view, name='forexpire'),
    path('inbox/analysis/return/<str:pk>/', inbox_views.return_pre_view, name='return_pre'),
    path('inbox/analysis/sign/<str:pk>/', inbox_views.sign_pre_view, name='sign_pre'),
    path('inbox/edit', inbox_views.edit_view, name='edit'),
    path('organizations/org/<str:pk>/noregister/', organizations_views.noregister_org_view, name='noregister_org'),
    path('inbox/sign', inbox_views.sign_view, name='sign'),
    path('inbox/sign/return/<str:pk>/', inbox_views.return_sign_view, name='return_sign'),
    path('inbox/analysis/registering/<str:pk>/', inbox_views.registering_view, name='registering_view'),
    path('inbox/sign/signing/<str:pk>/', inbox_views.signing_view, name='signing_view'),
    path('inbox/analysis/registering/<str:pk>/certificate/', inbox_views.Certificate_ROAC.as_view(), name='certificate'),

    #Comunicaciones
    path('comunication/users/', comunications_views.comunications_users_view, name='comunications_users'),
    path('comunication/orgs/', comunications_views.comunications_orgs_view, name='comunications_orgs'),

    #Eventos
    path('calendar/', events_views.general_calendar_view, name='calendar'),
    path('events/', events_views.events_view, name='events'),
    path('events/<str:pk>/', events_views.event_view, name='event'),
    path('events/<str:pk>/modify/', events_views.event_modify_view, name='modify_event'),
    path('events/<str:pk>/delete/', events_views.event_delete_view, name='delete_event'),

    #Actividades
    path('activities/', activities_views.activities_view, name='activities'),
    path('activities/<str:pk>/', activities_views.activity_view, name='activity'),
    path('activities/<str:pk>/modify/', activities_views.activity_modify_view, name='modify_activity'),
    path('activities/<str:pk>/delete/', activities_views.activity_delete_view, name='delete_activity'),

    #Visitas
    path('visits/', visits_views.visits_view, name='visits'),
    path('visits/<str:pk>/', visits_views.visit_view, name='visit'),
    path('visits/<str:pk>/modify/', visits_views.visit_modify_view, name='modify_visit'),
    path('visits/<str:pk>/delete/', visits_views.visit_delete_view, name='delete_visit'),
    path('visits/<str:pk>/create_act/', visits_views.create_act_view, name='create_act'),
    path('visits/<str:pk>/act/', visits_views.act_view, name='act'),

    #Reportes
    path('history/', history_views.history_view, name='history'),
    path('history/report/', history_views.Excel_report.as_view(), name='history_report'),
    path('visitsreport/', visits_views.visitsreport_view, name='visits_report'),
    path('visitsreport/report/', visits_views.Visits_excel_report.as_view(), name='visits_report_report'),
    path('eventsreport/', events_views.eventsreport_view, name='events_report'),
    path('eventsreport/report/', events_views.Events_excel_report.as_view(), name='events_report_report'),
    path('activitiesreport/', activities_views.activitiesreport_view, name='activities_report'),
    path('activitiesreport/report/', activities_views.Activities_excel_report.as_view(), name='activities_report_report'),

    #Reclamos
    path('claims/', claims_views.claims_view, name='claims'), 
    path('claims/multipleclaims/', claims_views.multipleclaims_views, name='multipleclaim'), 
    path('claim/<str:pk>/', claims_views.claim_view, name='claim'), 
    path('organizations/org/<str:pk>/setupclaim/', claims_views.setupclaim_view, name='setup_claim'), 
    path('claims/report/', claims_views.Excel_report.as_view(), name='claims_report'),
    path('claim/<str:pk>/modify/', claims_views.claim_modify_view, name='modify_claim'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)