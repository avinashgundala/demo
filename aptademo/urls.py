"""aptademo URL Configuration

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
from django.urls import path,re_path

########### import setting ############
from django.conf import settings
from django.conf.urls.static import static

########### import default viewe ############
from django.contrib.auth import views as auth_views

from webapp import views

urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', views.login, name='login'),

    ############ admin urls #########
    path('admin/', admin.site.urls),

    path('admin/home/', views.admin_create_user, name='admin_create_user'),

    re_path('admin/(?P<ID>[0-9]+)/product/(?P<status>[a-z,A-Z]+)/', views.admin_manage_product_status, name='admin_manage_product_status'),
    re_path('admin/manage/product/(?P<ID>[0-9]+)/delete/', views.admin_manage_product_delete, name='admin_manage_product_delete'),
    re_path('admin/manage/product/(?P<ID>[0-9]+)/update/', views.admin_manage_product_update, name='admin_manage_product_update'),
    path('admin/manage/product/', views.admin_manage_product, name='admin_manage_product'),


    re_path('admin/(?P<ID>[0-9]+)/permission/(?P<status>[a-z,A-Z]+)/', views.admin_manage_permissions_status, name='admin_manage_permissions_status'),
    re_path('admin/assign/permission/(?P<ID>[0-9]+)/delete/', views.admin_manage_permissions_delete, name='admin_manage_permissions_delete'),
    re_path('admin/assign/permission/(?P<ID>[0-9]+)/update/', views.admin_manage_permissions_update, name='admin_manage_permissions_update'),
    path('admin/assign/permission/', views.admin_manage_permissions, name='admin_manage_permissions'),
    path('admin/assign/permission/filter/', views.admin_manage_permissions_ajax, name='admin_manage_permissions_ajax'),


    # path('admin/assign_product/', views.admin_assign_product, name='admin_assign_product'),
    # path('admin/assign_product/filter/', views.admin_assign_permission, name='admin_assign_product_ajax'),


    # path('admin/assign/filter/',views.admin_assign_permission_ajax, name='admin_assign_permission_ajax'),
    # path('admin/manage/permission', views.admin_manage_permissions, name= 'admin_manage_permissions'),
    # path('admin/assign/form_submit',views.admin_assign_product_ajax, name='admin_assign_product_ajax'),

    ########### client urls #########
    path('client/', views.client_home, name='client_home'),
    #
    # ########## support urls #########
     path('agent/', views.agent_home, name='agent_home'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ [path('', views.login, name='Login'),]
