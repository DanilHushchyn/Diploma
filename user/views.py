from django.shortcuts import render, redirect
from user.forms import UserForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

def signin(request):
    return render(request, 'user/signin.html')


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('signin')
    user_form = UserForm()
    data = {'user_form': user_form}
    return render(request, 'user/register.html', context=data)


# class LoginUser(LoginView):
#     form_class = AuthenticationForm
#     template_name = 'user/signin.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Авторизация')
