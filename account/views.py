from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm  # Create a login form in forms.py
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, FriendRequest


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


def send_friend_request(request, to_username):
    from_user = request.user
    to_user = get_object_or_404(CustomUser, email=to_username)

    # Check if a friend request already exists
    existing_request = FriendRequest.objects.filter(from_user=from_user, to_user=to_user).first()
    if existing_request:
        print('Request already sent')
        # Handle case where a request already exists (e.g., redirect to a profile page)
        return JsonResponse({'request': 'already sent'})

    # Create a new friend request
    friend_request = FriendRequest(from_user=from_user, to_user=to_user)
    friend_request.save()
    print('Request added')
    # Redirect to a page indicating that the friend request has been sent
    return redirect('post:home')


def friend_request_list(request):
    current_user = request.user
    received_requests = FriendRequest.objects.filter(to_user=current_user, is_accepted=False)
    sent_requests = FriendRequest.objects.filter(from_user=current_user, is_accepted=False)

    return render(request, 'friend_request_list.html',
                  {'received_requests': received_requests, 'sent_requests': sent_requests})


def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user, is_accepted=False)

    # Accept the friend request
    friend_request.is_accepted = True
    friend_request.save()

    # Add each user to the other's friends list
    # friend_request.from_user.friends.add(request.user)
    request.user.friends.add(friend_request.from_user)

    return redirect('post:home')
