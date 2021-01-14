"""serverapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.auth import views
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.views.generic import RedirectView

# handler custom error message
# from django.conf.urls import handler404
# handler404 = 'igenlms.views.error_404_view'

urlpatterns = [
    path('igen_admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(template_name='registration/login.html'),
         name='login_user'),
    path('login/<str:next>/', views.LoginView.as_view(template_name='registration/login.html'),
         name='login_user'),
    path('logout/', views.LogoutView.as_view(next_page='/'), name='logout_user'),

    # reset password
    path('reset-password/', views.PasswordResetView.as_view(template_name='registration/reset_password.html',
    success_url=reverse_lazy('password_reset_done')), name='reset_password'),
    path('reset-password/done/', views.PasswordResetDoneView.as_view(template_name='registration/reset_password_done.html'),
        name='password_reset_done'),
    re_path(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', views.PasswordResetConfirmView.as_view(
        template_name='registration/reset_password_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
        # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', views.PasswordResetCompleteView.as_view(template_name='registration/reset_password_complete.html') ,
        name='password_reset_complete'),

    # change password
    path('dashboard/password-change/done/', views.PasswordChangeDoneView.as_view(template_name='registration/password_changedone.html'),
         name='password_change_done'),
    path('dashboard/password-change/', views.PasswordChangeView.as_view(template_name='registration/password_change.html',
                                                                        success_url=reverse_lazy('password_change_done')), name='password_change'),

    # restfull API
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('api/',include('webapi.urls')),

    # urls django app
    # path('', include('igenlms.urls')),
    # path('', RedirectView.as_view(pattern_name='dashboard'), name='home'),

    # django ckeditor
    # path('ckeditor', include('ckeditor_uploader.urls')),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
