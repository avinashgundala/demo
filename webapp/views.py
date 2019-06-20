from django.shortcuts import render,redirect,HttpResponse

from django.template.loader import render_to_string

########## Authentication #########
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager

from webapp.forms import *
from django.contrib.auth.decorators import login_required

from django.contrib import messages

######### send mail ############
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings

########## get domain #############
from django.contrib.sites.shortcuts import get_current_site

from webapp.decorators import admin_required,client_required,agent_required

from django.http import JsonResponse

from webapp.models import *

# #-------------------- Authentication ------------------#
def login(request):
    """
    This view to validate the login credentials of the user

    """
    if request.method =='POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    if user.user_type == 'Admin':
                        auth_login(request, user)
                        if 'next' in request.GET and request.GET['next']:
                            return redirect(request.GET['next'])
                        return redirect('admin_create_user')
                    elif user.user_type == 'Agent':
                        auth_login(request, user)
                        if 'next' in request.GET and request.GET['next']:
                            return redirect(request.GET['next'])
                        return redirect('agent_home')
                    elif user.user_type == 'Client':
                        auth_login(request, user)
                        if 'next' in request.GET and request.GET['next']:
                            return redirect(request.GET['next'])
                        return redirect('client_home')
                    else:
                        return redirect('login')
                else:
                    messages.add_message(request, messages.ERROR,'Your Account is not Activated admin will active your account with in 24 hours.' )
            else:
                messages.add_message(request, messages.ERROR,'Your Email or Password is Incorrect.' )
    else:
        login_form = LoginForm()

    context = {
        'login_form':login_form
    }
    return render(request,'registration/login.html',context)

# #------------------------ admin ---------------------------#


def admin_home(request):
    pass


@login_required
@admin_required
def admin_create_user(request):
    if request.method == 'POST':
        usertype =  request.POST.get('user_type')
        password1 = request.POST.get('password1')
        form = ClientAgentSignupForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_type = usertype
            form.save()

            subject = 'Thank you for registering to our site'
            message = 'email: {},password: {}'.format(form.email,password1)
            email_from = settings.EMAIL_HOST_USER
            email_user = form.email
            recipient_list = [email_user,]
            send_mail( subject, message, email_from, recipient_list)

            messages.add_message(request,messages.SUCCESS,'User %s added successfully' %(form.first_name))

            return redirect('admin_manage_permissions')
        else:
            print(form.errors)
    else:
        password =  BaseUserManager().make_random_password(8)
        form = ClientAgentSignupForm()
    arg = {
     'password1':password,
     'form':form
    }
    return render(request,'admin/admin_create_user.html',arg)

@admin_required
@login_required
def admin_manage_product(request):
    form_error = False
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form = product_form.save()
            #message
            return redirect('admin_manage_product')
        else:
            form_error = True
    else:
        product_form = ProductForm()
    arg = {
            'product_form':product_form,
            'Instance_product':Product.objects.all()
    }
    return render(request,'admin/admin_mange_product.html')

@admin_required
@login_required
def admin_manage_product_update(request,ID):
    instance_product = Product.objects.get(id=ID)
    if request.method == 'POST':
        product_form = ProductForm(request.POST,instance=instance_product)
        if product_form.is_valid():
            product_form = product_form.save()
            #message
            return redirect('admin_manage_product')
    else:
        product_form = ProductForm(instance=instance_product)
    arg = {
        'product_form':product_form
    }
    return render(request,'admin/admin_manage_product_update.html')

@admin_required
@login_required
def admin_manage_product_status(request,ID,status):
    instance_product = Product.objects.get(id=ID)
    if status == 'True':
        instance_product.is_active = True
        instance_product.save()
        #message
    elif status == 'False':
        instance_product.is_active = False
        intance_product.save()
        #message
    return redirect('admin_manage_product')

@admin_required
@login_required
def admin_manage_product_delete(request,ID):
    instance_product = Product.objects.get(id=ID)
    instance_product.delete()
    #message
    return redirect('admin_manage_product')

@admin_required
@login_required
def admin_manage_permissions(request):
    form = False
    get_user_id = request.GET.get('user_name','')
    instance_users = User.objects.all().exclude(user_type='Admin')
    instance_permissions = AssignProduct.objects.all()
    if request.method == 'POST':
        assign_form = AssignProductForm(request.POST)
        if assign_form.is_valid():
            assign_form = assign_form.save(commit=False)
            instance_users = instance_users.get(id=get_user_id)
            assign_form.user = instance_users
            assign_form.save()
            #messages
            return redirect('admin_manage_permissions')
    else:
        assign_form = AssignProductForm()
    arg = {
            'assign_form':assign_form,
            'instance_users':instance_users,
            'instance_permissions':instance_permissions,

    }
    return render(request,'admin/admin_manage_permissions.html',arg)

def admin_manage_permissions_ajax(request):
    data = dict()
    get_user_id = request.GET.get('user_name','')
    if request.is_ajax():
        instance_users = User.objects.all().exclude(user_type='Admin')
        if get_user_id:
            instance_users = instance_users.get(id=get_user_id)
        data['instance_users'] = instance_users.user_type
        return JsonResponse(data)

@admin_required
@login_required
def admin_manage_permissions_update(request,ID):
    instance_assign_product = AssignProduct.objects.get(id=ID)
    if request.method == 'POST':
        assign_form = AssignProductForm(request.POST,instance=instance_assign_product)
        if assign_form.is_valid():
            assign_form = assign_form.save(commit=False)
            assign_form.save()
            #messages
            return redirect('admin_manage_permissions')
    else:
        assign_form = AssignProductForm(instance=instance_assign_product)
    arg = {
            'assign_form':assign_form,
    }
    return render(request,'admin/admin_manage_permissions_update.html',arg)

@admin_required
@login_required
def admin_manage_permissions_status(request,ID,status):
    instance_assign_product = AssignProduct.objects.get(id=ID)
    if status == 'True':
        instance_assign_product.status = True
        instance_assign_product.save()
    elif status == 'False':
        instance_assign_product.status = False
        instance_assign_product.save()
    return redirect('admin_manage_permissions')

@admin_required
@login_required
def admin_manage_permissions_delete(request,ID):
    instance_assign_product = AssignProduct.objects.get(id=ID)
    instance_assign_product.delete()
    return redirect('admin_manage_permissions')


# @admin_required
# @login_required
# def admin_assign_product(request):
#     form = False
#     get_user_id = request.GET.get('user_name','')
#     instance_users = User.objects.all().exclude(user_type='Admin')
#     if get_user_id:
#         instance_users = instance_users.get(id=get_user_id)
#     if request.method == "POST":
#         product_form = ProductForm(request.POST)
#         if product_form.is_valid():
#             product_form.save()
#             return redirect('admin_assign_product')
#         else:
#             form = True
#     else:
#         product_form = ProductForm()
#     arg= {
#         'product_form':product_form,
#         'instance_users':instance_users
#     }
#     return render(request,'admin/admin_assign_product.html')
#
# @admin_required
# @login_required
# def admin_assign_product_ajax(request):
#     data = dict()
#     get_user_id = request.GET.get('user_name','')
#     if request.is_ajax():
#         instance_users = User.objects.all().exclude(user_type='Admin')
#         if get_user_id:
#             instance_users = instance_users.get(id=get_user_id)
#         data['instance_users'] = instance_users.user_type
#         return JsonResponse(data)
#
# @login_required
# @admin_required
# def admin_assign_permission(request):
#     get_user_id = request.GET.get('user_name','')
#     instance_users = User.objects.all().exclude(user_type='Admin')
#     if get_user_id:
#         instance_users = instance_users.get(id=get_user_id)
#
#     arg = {
#         'instance_users':instance_users
#     }
#     return render(request,'admin/admin_assign_permission.html',arg)
#
# def admin_assign_permission_ajax(request):
#     data = dict()
#     get_user_id = request.GET.get('user_name','')
#     if request.is_ajax():
#         instance_users = User.objects.all().exclude(user_type='Admin')
#         if get_user_id:
#             instance_users = instance_users.get(id=get_user_id)
#         data['instance_users'] = instance_users.user_type
#         return JsonResponse(data)
#
#
# # def admin_create_product_user(request):
# #     get_user_id = request.GET.get('user_name','')
# #     get_product_list = request.GET.get('product','')
# #     get_email_list = request.GET.getlist('email_name','')
# #     get_password_list = request.GET.getlist('password_name','')
# #     get_alert_list = request.GET.getlist('alert_name','')
# #     user = User.objects.get(id=get_user_id)
# #     for i in range(len(get_product_list)):
# #         product = get_product_list[i]
# #         email = get_email_list[i]
# #         password = get_password_list[i]
# #         if get_alert_list is not None:
# #             alert = get_alert_list[i]
# #             instance_product = Product(user=user, products=product, email=email, password=password,alert=alert)
# #             instance_product.save()
# #         else:
# #             instance_product = Product(user=user, products=product, email=email, password=password)
# #             instance_product.save()
# #
# #
# #     subject = 'Thank you for registering to our site'
# #     message = 'email: {},password: {}'.format(user.email,password1)
# #     email_from = settings.EMAIL_HOST_USER
# #     email_user = user.email
# #     recipient_list = [email_user,]
# #     send_mail( subject, message, email_from, recipient_list)
# #
# #     return redirect('admin_manage_permissions')
# #
# # def admin_manage_permissions(request):
# #     return render(request,'admin/admin_manage_permissions.html')
#
#
#
#
#
#
#
# # def admin_assign_product_ajax(request):
# #     data = dict()
# #     if request.method == 'POST':
# #         product_form = ProductForm(request.POST)
# #         if product_form.is_valid():
# #             product_form = product_form.save()
# #             data['form_is_valid'] = True
# #
# #             subject = 'Thank you for registering to our site'
# #             message = 'product:{}, email: {}, password: {}'.format(product_form.products, product_form.email, product_form.password)
# #             email_from = settings.EMAIL_HOST_USER
# #             email_user = product_form.user.email
# #             recipient_list = [email_user,]
# #             send_mail( subject, message, email_from, recipient_list )
# #
# #
# #             context = {
# #                'product':product_form.products
# #             }
# #             data['html_created_product'] = render_to_string('admin/admin_assign_product_filter.html',
# #             context)
# #
# #
# #         else:
# #             print(product_form.errors)
# #             print("error")
# #
# #     return JsonResponse(data)
#
#
#
@login_required
@client_required
def client_home(request):
    product_credentials=[]
    instance_assign_product = AssignProduct.objects.filter(user=request.user)
    for i in instance_assign_product:
        product_name = i.product.name
        username = i.email
        url = i.product.url
        password = i.password
        product_credentials.append({'product_name':product_name,'username':username,'password':password,'url':url})
    print(product_credentials)
    arg = {
            'product_credentials':product_credentials,
    }
    return render(request,'client/client-home.html',arg)

@login_required
@agent_required
def agent_home(request):
    product_credentials=[]
    instance_assign_product = AssignProduct.objects.filter(user=request.user)
    for i in instance_assign_product:
        product = i.product.name
        username = i.email
        url = i.product.url
        password = i.password
        product_credentials.append({'product_name':product_name,'username':username,'password':password,'url':url})
    print(product_credentials)
    arg = {
            'product_credentials':product_credentials,
    }
    return render(request,'agent/agent-home.html',arg)
