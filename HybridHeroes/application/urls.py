from django.urls import path, include
from django.conf.urls import url
from .views import (
    view_dashboard,
    view_home,
    view_queue,
    view_privacy,
    view_requests,
    view_responses,
    view_login,
    view_logout,
    view_signup,
    view_activate,
    view_profile,
    view_request_description,
    view_add_update_request,

    view_add_to_queue_required,
    view_delete_from_queue_required,
    view_delete_request_required,
    view_delete_response_required,
    view_add_response_required,
)
from django.contrib.auth import views as auth_views

app_name = 'application'

urlpatterns = [

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        view_activate, name='activate'),

    path('', view_home, name='home'),
    path('dashboard/', view_dashboard, name='dashboard'),
    path('profile/', view_profile, name='profile'),
    path('dashboard/<int:pk>/', view_dashboard, name='dashboard-specific'),
    path('queue/', view_queue, name='queue'),
    path('privacy/', view_privacy, name='privacy'),
    path('requests/', view_requests, name='requests'),
    path('add/request/', view_add_update_request, name='add-request'),
    path('update/request/<int:pk>/', view_add_update_request, name='update-request'),
    path('request/description/<int:pk>/', view_request_description, name='request-description'),
    path('responses/', view_responses, name='responses'),
    path('response/', view_responses, name='response'),
    path('accounts/login/', view_login, name='login'),
    path('accounts/logout/', view_logout, name='logout'),

    path('signup/', view_signup, name='signup'),
    path('update/request/', view_responses, name='update-request'),
    path('settings/', view_privacy, name='settings'),

    path('delete/request/<int:pk>/', view_delete_request_required, name='delete-request-required'),
    path('delete/response/<int:req_id>/<int:res_id>/', view_delete_response_required, name='delete-response-required'),
    path('queue/add/<int:pk>/', view_add_to_queue_required, name='add-to-queue-required'),
    path('add/response/<int:pk>/', view_add_response_required, name='add-response-required'),
    path('queue/delete/<int:pk>/', view_delete_from_queue_required, name='delete-from-queue-required'),

    path(
        'change-password/', auth_views.PasswordChangeView.as_view(
            template_name='application/password_change.html',
            success_url='/'
        ), name='change_password'
    ),
]
