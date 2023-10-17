from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views
from .views import autocomplete_university

urlpatterns = [
    path('logout', views.logout, name='user_logout'),
    path('login', views.user_login, name='user_login'),
    path('signup', views.signup, name='signup'),
    path('accounts/activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    url(r'accounts/activate/sent/$', views.account_activation_sent, name='account_activation_sent'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset', ),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done', ),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm', ),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete', ),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html')),
    url(r'^ajax_calls/search_university/', autocomplete_university),
]
