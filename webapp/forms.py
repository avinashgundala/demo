from django import forms

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms  import UserCreationForm

from webapp.models import *

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"input", 'autocomplete':"nope", "placeholder":"Email address"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input", 'autocomplete':"new-password", "placeholder":"*************" }))

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = {
                    'email',
                    'password1',
                    'password2',
                    'first_name',
                    'user_type',
        }
        widgets = {
                'email' :forms.EmailInput(attrs={"id":"email", "class":"input100", 'autocomplete':"nope", 'placeholder':"Email", 'required':'required'}),
                'first_name' :forms.TextInput(attrs={"id":"firstname", "class":"input100", 'autocomplete':"nope", 'placeholder':"First Name", 'required':'required','autofocus':True}),
                'user_type' :forms.SelectMultiple(attrs={"class":"js-select2"}),
            }

class ClientAgentSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = {
                   'email',
                   'first_name',
                   'password1',
                   'password2',
        }
        widgets = {
            'email' :forms.EmailInput(attrs={"id":"email",'autocomplete':"nope",'class':'input100','placeholder':"Email", 'required':'required'}),
            'first_name' :forms.TextInput(attrs={"id":"firstname",'autocomplete':"nope",'class':'input100','placeholder':"Full Name", 'required':'required','autofocus':True}),

        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = {
                'product_name',
                'description',
                'url',
        }
        widgets = {
            'product_name':forms.TextInput(attrs={}),
            'description':forms.Textarea(attrs={}),
        }


class AssignProductForm(forms.ModelForm):
    class Meta:
        model = AssignProduct
        fields = {
                   'product',
                   'email',
                   'password',
                   'alert',
        }
