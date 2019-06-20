from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from webapp.models import *

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'Admin':
            return function(request, *args, **kwargs)
        elif request.user.user_type == 'Client':
            return redirect('client_home')
        elif request.user.user_type == 'Agent':
            return redirect('agent_home')
        else:
            return redirect('logout')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def client_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'Admin':
            return redirect('admin_home')
        elif request.user.user_type == 'Client':
            return function(request, *args, **kwargs)
        elif request.user.user_type == 'Agent':
            return redirect('agent_home')
        else:
            return redirect('logout')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def agent_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 'Admin':
            return redirect('admin_home')
        elif request.user.user_type == 'Client':
            return redirect('client_home')
        elif request.user.user_type == 'Agent':
            return function(request, *args, **kwargs)
        else:
            return redirect('logout')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
