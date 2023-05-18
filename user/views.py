from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from django.contrib.auth.mixins import AccessMixin

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from admin_panel.models import *
from user.forms import *


#
#
class SignUp(CreateView):
    model = Account
    form_class = UserForm
    context_object_name = 'user_form'
    template_name = "../templates/user/register.html"
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


#
# class SignIn(LoginView):
#     template_name = '../templates/user/signin.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('main')
#         if request.method == 'POST':
#             return self.post(request, *args, **kwargs)
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         error = False
#         form = SignInForm(request.POST)
#         print(form.fields['email'])
#         print('POST')
#         print(request.POST['email'])
#         print('POST',form.error_messages)
#         print('POST',form)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             print('IS VALID')
#             user = authenticate(email=email, password=password)
#             if user:
#                 print('IS AUTHENTICATED')
#
#                 login(request, user)
#                 return redirect('main')
#             else:
#                 error = True
#         else:
#             form = SignInForm()
#         data = {
#             'form': form,
#             'error': error,
#             'banner':getBanner()
#         }
#         return render(request, '../templates/user/signin.html', context=data)
#
#     def get_success_url(self):
#         return reverse_lazy('main')

def loginView(request):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_obj = authenticate(email=email, password=password)
            if user_obj:
                login(request, user_obj)
                if user_obj.is_staff:
                    return redirect('statistic')
                if request.GET.get('next', None) is None:
                    return redirect('main')
                else:
                    return redirect(request.GET.get('next', None))
        else:
            data = {
                'form': form,
            }
            return render(request, '../templates/user/signin.html', context=data)

    else:
        form = SignInForm()
    data = {
        'form': form,
    }
    return render(request, '../templates/user/signin.html', context=data)


def logoutView(request):
    logout(request)
    return redirect('main')


class SignOut(LogoutView):
    redirect_field_name = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
