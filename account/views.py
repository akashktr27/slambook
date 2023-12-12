from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm  # Create a login form in forms.py
from django.contrib.auth import logout
from django.urls import reverse
# Create your views here.

class SignUpView(TemplateView):
    template_name = 'account/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_data'] = 'This is custom data!'

        return context

    def get(self, request, *args, **kwargs):
        # Handle GET requests here
        user = request

        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        # Handle POST requests here
        # You can access form data using request.POST

        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')

        else:
            return self.get(request)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email)
            print(password)
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                # Redirect to a success page or home page after successful login
                print('Login success')
                return redirect('post:home')
            else:
                messages.error(request, 'Invalid email or password.')

    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    # Logout the user
    logout(request)
    # Redirect to a specific page after logout
    return redirect(reverse('account:login'))

